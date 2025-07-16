# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: utils_sqlalchemy.py
@time: 2025/6/15 21:16 
@desc: 

"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from contextlib import asynccontextmanager
from typing import AsyncGenerator, List, Optional, Dict
from models.model_db import DatabaseConfig, get_db_config
from models.tables.model_base import Base
from fastapi import Depends
from sqlalchemy import select, text, update, inspect


class AsyncSqlAlchemyUtils:
    """
    异步SQLAlchemy工具类
    """

    def __init__(self, host, port, user, password, database, pool_size=50, debug=False):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.pool_size = pool_size
        self.debug = debug

        self.engine = None
        self.async_session = None
        self.create_async_engine()
        self._init_async_session()

    def create_async_engine(self):
        """创建异步引擎"""
        if not self.engine:
            self.engine = create_async_engine(
                f"mysql+aiomysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}",
                echo=self.debug,
                pool_size=self.pool_size,
                future=True
            )

    async def _create_tables(self):
        """异步创建所有表"""
        async with self.engine.begin() as conn:
            if not await conn.run_sync(
                    lambda sync_conn: inspect(sync_conn).has_table("CardSecret")
            ):
                await conn.run_sync(Base.metadata.create_all)

    def _init_async_session(self):
        """初始化异步会话工厂"""
        if self.engine is not None and self.async_session is None:
            self.async_session = async_sessionmaker(
                bind=self.engine,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False
            )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        获取异步数据库会话
        """
        if self.async_session is None:
            raise RuntimeError("Async session not initialized!")

        session = self.async_session()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def run_raw_sql(self, sql: str, params: dict = None, is_query=False):
        """
        异步执行原生SQL
        """
        async with self.get_session() as session:
            result = await session.execute(text(sql), params or {})
            if is_query:
                return result.mappings().all()
            return result.rowcount

    async def query_by_conditions(self, model: Base, filters: Optional[Dict] = None,
                                  status: object = True) -> List[Base]:
        """
        异步条件查询
        """
        async with self.get_session() as session:
            query = select(model)
            if filters:
                conditions = [getattr(model, key) == value for key, value in filters.items()]
                query = query.where(*conditions)

            result = await session.execute(query)
            return result.scalars().all() if status else [result.scalars().first()]

    async def insert_object(self, obj: Base) -> int:
        """
        异步插入单个对象
        """
        async with self.get_session() as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)  # 刷新获取自动生成的ID

            # 获取ID，假设主键字段名为'id'
            obj_id = getattr(obj, 'id', None)

            return (1, obj_id) if obj_id is not None else (1, None)

    async def insert_objects(self, objs: List[Base]) -> int:
        """
        异步批量插入对象
        """
        if not objs:
            return 0, []

        inserted_ids = []
        async with self.get_session() as session:
            try:
                # 批量添加对象
                session.add_all(objs)
                await session.commit()

                # 获取所有插入对象的ID
                inserted_ids = [obj.id for obj in objs if hasattr(obj, 'id') and obj.id is not None]
                print("inserted_ids", len(objs), inserted_ids)

                return len(objs), inserted_ids

            except Exception as e:
                await session.rollback()
                # 尝试逐个插入以获取部分成功的结果
                print(e)
                success_count = 0
                for obj in objs:
                    print("obj",obj)
                    try:
                        session.add(obj)
                        await session.commit()
                        if hasattr(obj, 'id') and obj.id is not None:
                            inserted_ids.append(obj.id)
                        success_count += 1
                    except Exception as e:
                        await session.rollback()
                        continue

                return success_count, inserted_ids

    async def update_objects(self, objs: List[Base]) -> int:
        """
        异步批量更新对象
        """
        if not objs:
            return 0, []

        updated_ids = []
        async with self.get_session() as session:
            model_class = type(objs[0])
            primary_key = model_class.__table__.primary_key.columns.keys()[0]
            updated_count = 0

            for obj in objs:
                # 检查对象是否有ID
                obj_id = getattr(obj, primary_key)
                if obj_id is None:
                    continue

                # 检查记录是否存在
                exists = await session.execute(
                    select(model_class).where(
                        getattr(model_class, primary_key) == obj_id
                    )
                )
                if not exists.scalar_one_or_none():
                    continue

                # 准备更新值，排除内部属性和主键
                update_values = {
                    k: v for k, v in obj.__dict__.items()
                    if not k.startswith('_') and k != primary_key
                }

                # 检查是否有实际需要更新的字段
                if not update_values:
                    continue

                # 执行更新
                update_stmt = (
                    update(model_class)
                    .where(getattr(model_class, primary_key) == obj_id)
                    .values(**update_values)
                    .execution_options(synchronize_session=False)
                )

                result = await session.execute(update_stmt)
                if result.rowcount > 0:
                    updated_count += 1
                    updated_ids.append(obj_id)

            await session.commit()
            return updated_count, updated_ids


async def get_async_db(config: DatabaseConfig = Depends(get_db_config)) -> AsyncSqlAlchemyUtils:
    """获取异步数据库工具实例"""
    return AsyncSqlAlchemyUtils(**config.dict())
