from typing import Optional

from specter.crud.base import CRUDBase
from specter.models import AccountUser
from specter.schemas import AccountUserCreate, AccountUserUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDAccountUser(CRUDBase[AccountUser, AccountUserCreate, AccountUserUpdate]):  # type: ignore

    async def get_by_email(
        self, db: AsyncSession, *, email: str
    ) -> Optional[AccountUser]:
        """

        Args:
            db:
            email:

        Returns:

        """
        stmt = select(self.model).where(self.model.email == email)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()


account_user = CRUDAccountUser(AccountUser)
