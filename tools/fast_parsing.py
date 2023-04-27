

from typing import Optional


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Group, Teacher, Office

from tools.other import other


class FastParsing:
    @staticmethod
    async def get_group_by_id(session: AsyncSession, ido: int) -> Optional[Group]:
        stmt = select(Group).where(Group.id == ido)
        result = await session.execute(stmt)
        return result.scalar()

    @staticmethod
    async def get_group_name_by_id(session: AsyncSession, ido: int) -> Optional[str]:
        stmt = select(Group.name).where(Group.id == ido)
        result = await session.execute(stmt)
        return result.scalar()

    @staticmethod
    async def get_group_id_by_name(session: AsyncSession, name: str) -> Optional[int]:
        stmt = select(Group)
        result = await session.execute(stmt)
        groups = result.fetchall()
        return other.check_groups_in_groups_list(name, groups)

    @staticmethod
    async def get_teacher_by_id(session: AsyncSession, ido: str) -> Optional[Teacher]:
        stmt = select(Teacher).where(Teacher.id == ido)
        result = await session.execute(stmt)
        return result.scalar()

    @staticmethod
    async def get_teacher_name_by_id(session: AsyncSession, ido: str) -> Optional[str]:
        stmt = select(Teacher.name).where(Teacher.id == ido)
        result = await session.execute(stmt)
        return result.scalar()

    @staticmethod
    async def get_teacher_id_by_name(session: AsyncSession, name: str) -> Optional[int]:
        stmt = select(Teacher.id).where(Teacher.name.ilike(f"%{name}%"))
        result = await session.execute(stmt)
        return result.scalar()

    @staticmethod
    async def get_office_by_id(session: AsyncSession, ido: int) -> Optional[Teacher]:
        stmt = select(Office).where(Office.id == ido)
        result = await session.execute(stmt)
        return result.scalar()

    @staticmethod
    async def get_office_name_by_id(session: AsyncSession, ido: int) -> Optional[str]:
        stmt = select(Office.name).where(Office.id == ido)
        result = await session.execute(stmt)
        return result.scalar()

    @staticmethod
    async def get_office_id_by_name(session: AsyncSession, name: str) -> Optional[int]:
        stmt = select(Office.id).where(Office.name.ilike(f"%{name}%"))
        result = await session.execute(stmt)
        return result.scalar()


fast_parsing = FastParsing()
