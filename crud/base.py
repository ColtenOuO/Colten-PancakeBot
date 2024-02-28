from pydantic import BaseModel

from typing import Generic, TypeVar

SchemaType = TypeVar("SchemaType", bound=BaseModel)


class CRUDBase(Generic[SchemaType]):
    @staticmethod
    def create() -> SchemaType:
        pass

    @staticmethod
    def get() -> SchemaType:
        pass

    @staticmethod
    def update() -> SchemaType:
        pass

    @staticmethod
    def delete():
        pass
