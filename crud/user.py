from schemas.user import User

from .base import CRUDBase

class CRUDUser(CRUDBase[User]):
    @staticmethod
    def get(user_id: int) -> User:
        pass


