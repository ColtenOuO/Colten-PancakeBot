from motor.core import AgnosticCollection
from pydantic import BaseModel

from types import NoneType
from typing import Generic, Optional, TypeVar, Union

from database.database import DB

SchemaType = TypeVar("SchemaType", bound=BaseModel)
SchemaUpdateType = TypeVar("SchemaUpdateType", bound=BaseModel)


class CRUDBase(Generic[SchemaType, SchemaUpdateType]):
    collection: AgnosticCollection
    _schema_cls: BaseModel

    def __init__(self, collection_name: str, schema_cls: SchemaType) -> None:
        self.collection = DB[collection_name]
        self._schema_cls = schema_cls

    async def create(self, data: SchemaType) -> SchemaType:
        await self.collection.insert_one(data.model_dump())
        return data

    async def create_many(self, data_list: list[SchemaType]) -> list[SchemaType]:
        await self.collection.insert_many(list(map(
            lambda data: data.model_dump(), data_list
        )))
        return data_list

    async def get(
        self,
        query: Union[SchemaUpdateType, dict]
    ) -> Optional[SchemaType]:
        result = await self.collection.find_one(
            query if type(query) is dict else
            query.model_dump(exclude_unset=True),
            {"_id": 0}
        )

        if result is None:
            return None
        return self._schema_cls(**result)

    async def get_many(
        self,
        query: Union[SchemaUpdateType, dict],
        limit: int = 10
    ) -> list[SchemaType]:
        cursor = self.collection.find(
            query if type(query) is dict
            else query.model_dump(exclude_unset=True),
            {"_id": 0}
        )

        results = await cursor.to_list(max(1, limit))
        return list(map(lambda result: SchemaType(**result), results))

    async def update(
        self,
        query: Union[SchemaUpdateType, dict],
        update: SchemaUpdateType
    ) -> SchemaType:
        await self.collection.find_one_and_update(
            query if type(query) is dict
            else query.model_dump(exclude_unset=True),
            {"$set" : update if type(update) is dict
            else update.model_dump(exclude_unset=True)}
        )

        return await self.get(query)

    async def delete(
        self,
        query: Union[SchemaUpdateType, dict]
    ) -> NoneType:
        await self.collection.delete_one(
            query if type(query) is dict
            else query.model_dump(exclude_unset=True)
        )

    async def delete_many(
        self,
        query: Union[SchemaUpdateType, dict]
    ) -> NoneType:
        await self.collection.delete_many(
            query if type(query) is dict
            else query.model_dump(exclude_unset=True)
        )
