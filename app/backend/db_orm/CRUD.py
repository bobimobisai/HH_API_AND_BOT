from sqlalchemy.future import select
from backend.db_orm.Connector import async_session_factory
from backend.db_orm.Models import UserOrm, NoteOrm, TagOrm
import uuid


class UserCRUD:
    @staticmethod
    async def create_user(
        tg_user_id: int,
        email: str,
        password_hash: str,
        first_name: str,
        last_name: str,
        username: str,
    ):
        async with async_session_factory() as session:
            new_user = UserOrm(
                tg_user_id=tg_user_id,
                email=email,
                password_hash=password_hash,
                first_name=first_name,
                last_name=last_name,
                username=username,
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user

    @staticmethod
    async def get_user_by_email(email: str):
        async with async_session_factory() as session:
            result = await session.execute(
                select(UserOrm).where(UserOrm.email == email)
            )
            return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_tg_user_id(tg_user_id: int):
        async with async_session_factory() as session:
            result = await session.execute(
                select(UserOrm).where(UserOrm.tg_user_id == tg_user_id)
            )
            return result.scalar_one_or_none()

    @staticmethod
    async def update_user(user_id: uuid.UUID, **kwargs):
        async with async_session_factory() as session:
            user = await session.get(UserOrm, user_id)
            if user:
                for key, value in kwargs.items():
                    setattr(user, key, value)
                await session.commit()
                await session.refresh(user)
            return user

    @staticmethod
    async def delete_user(user_id: uuid.UUID):
        async with async_session_factory() as session:
            user = await session.get(UserOrm, user_id)
            if user:
                await session.delete(user)
                await session.commit()
            return user


class NoteCRUD:
    @staticmethod
    async def create_note(
        user_id: uuid.UUID, title: str, text: str, tags: list[str] = None
    ):
        async with async_session_factory() as session:
            new_note = NoteOrm(user_id=user_id, title=title, text=text)

            # Обработка тегов
            if tags:
                existing_tags = await session.execute(
                    select(TagOrm).where(TagOrm.name.in_(tags))
                )
                existing_tags = existing_tags.scalars().all()

                new_tags = [
                    TagOrm(name=tag)
                    for tag in tags
                    if tag not in {t.name for t in existing_tags}
                ]
                new_note.tags.extend(existing_tags + new_tags)

            session.add(new_note)
            await session.commit()
            await session.refresh(new_note)
            return new_note

    @staticmethod
    async def get_note_by_id(note_id: uuid.UUID):
        async with async_session_factory() as session:
            result = await session.execute(select(NoteOrm).where(NoteOrm.id == note_id))
            return result.scalar_one_or_none()

    @staticmethod
    async def get_notes_by_user(user_id: uuid.UUID):
        async with async_session_factory() as session:
            result = await session.execute(
                select(NoteOrm).where(NoteOrm.user_id == user_id)
            )
            return result.scalars().all()

    @staticmethod
    async def update_note(note_id: int, **kwargs):
        async with async_session_factory() as session:
            note = await session.get(NoteOrm, note_id)
            if note:
                for key, value in kwargs.items():
                    setattr(note, key, value)
                await session.commit()
                await session.refresh(note)
            return note

    @staticmethod
    async def delete_note(note_id: int):
        async with async_session_factory() as session:
            note = await session.get(NoteOrm, note_id)
            if note:
                await session.delete(note)
                await session.commit()
            return note


class TagCRUD:
    @staticmethod
    async def create_tag(name: str):
        async with async_session_factory() as session:
            new_tag = TagOrm(name=name)
            session.add(new_tag)
            await session.commit()
            await session.refresh(new_tag)
            return new_tag

    @staticmethod
    async def get_tag_by_id(tag_id: uuid.UUID):
        async with async_session_factory() as session:
            result = await session.get(TagOrm, tag_id)
            return result

    @staticmethod
    async def get_tag_by_name(name: str):
        async with async_session_factory() as session:
            result = await session.execute(select(TagOrm).where(TagOrm.name == name))
            return result.scalar_one_or_none()

    @staticmethod
    async def update_tag(tag_id: uuid.UUID, **kwargs):
        async with async_session_factory() as session:
            tag = await session.get(TagOrm, tag_id)
            if tag:
                for key, value in kwargs.items():
                    setattr(tag, key, value)
                await session.commit()
                await session.refresh(tag)
            return tag

    @staticmethod
    async def delete_tag(tag_id: uuid.UUID):
        async with async_session_factory() as session:
            tag = await session.get(TagOrm, tag_id)
            if tag:
                await session.delete(tag)
                await session.commit()
            return tag

    @staticmethod
    async def get_all_tags():
        async with async_session_factory() as session:
            result = await session.execute(select(TagOrm))
            tags = result.scalars().all()
            return tags
