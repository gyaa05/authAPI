from sqlalchemy import Column, Integer, String, select, update, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession

from models.db_session import SqlAlchemyBase as Base


class OrganisationCred(Base):
    __tablename__ = 'organisation_creds'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    @classmethod
    async def get_by_login(cls, login: str, session: AsyncSession):

        _ = await session.execute(select(cls).where(cls.login == login))
        return _.scalar()

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()
