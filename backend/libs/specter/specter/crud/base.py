from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union, cast

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from specter.db.base_class import Base
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        """
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """

        Args:
            db:
            id:

        Returns:

        """
        stmt = select(self.model).where(getattr(self.model, "id") == id)
        result = await db.execute(stmt)
        return cast(Optional[ModelType], result.scalar_one_or_none())

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """

        Args:
            db:
            obj_in:

        Returns:

        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return cast(ModelType, db_obj)

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """

        Args:
            db:
            db_obj:
            obj_in:

        Returns:

        """
        # obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: Any) -> Optional[ModelType]:
        """

        Args:
            db:
            id:

        Returns:

        """
        obj = await self.get(db=db, id=id)
        if obj is not None:
            await db.delete(obj)
            await db.commit()
        return obj
