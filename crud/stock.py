from typing import Optional

from schemas import Stock, StockUpdate

from .base import CRUDBase



class CRUDStock(CRUDBase[Stock, StockUpdate]):
    def __init__(self) -> None:
        super().__init__("stock_data", Stock)

    async def get_all_code(
        self,
        offset: int = 0,
        limit: Optional[int] = 10
    ) -> list[str]:
        cursor = self.collection.find(
            {}, {"_id": 0, "code": 1}
        ).skip(offset or 0)

        if limit:
            cursor = cursor.limit(limit)
        result = await cursor.to_list(None)
        return list(map(lambda data: data["code"], result))

    async def get_by_code(self, code: str) -> Optional[Stock]:
        result = await self.get(StockUpdate(code=code))

        return result

    async def update_by_code(self, code: str, update: StockUpdate) -> Optional[Stock]:
        result = await self.update(StockUpdate(code=code), update)

        return result
