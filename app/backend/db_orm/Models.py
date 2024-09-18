from sqlalchemy.orm import Mapped, mapped_column
from backend.db_orm.Connector import Base, str_256
from sqlalchemy import BigInteger, Column, text, ForeignKey, Boolean, String, Table
from sqlalchemy.dialects.postgresql import UUID
import datetime
import uuid
from typing import Annotated
from enum import Enum
from sqlalchemy.orm import relationship, backref


intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]
updated_at = Annotated[
    datetime.datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow(),
    ),
]
note_tag_association = Table(
    "note_tag_association",
    Base.metadata,
    Column("note_id", UUID(as_uuid=True), ForeignKey("note.id"), primary_key=True),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tag.id"), primary_key=True),
)


class UserOrm(Base):
    __tablename__ = "user"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tg_user_id: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
        index=True,
        unique=True,
    )
    email: Mapped[str] = mapped_column(
        String(256), nullable=False, unique=True, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False, index=True)
    last_name: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    notes: Mapped[list["NoteOrm"]] = relationship(
        "NoteOrm", back_populates="user", cascade="all, delete-orphan"
    )


class NoteOrm(Base):
    __tablename__ = "note"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["UserOrm"] = relationship("UserOrm", back_populates="notes")

    tags: Mapped[list["TagOrm"]] = relationship(
        "TagOrm", secondary=note_tag_association, back_populates="notes"
    )


class TagOrm(Base):
    __tablename__ = "tag"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    notes: Mapped[list["NoteOrm"]] = relationship(
        "NoteOrm", secondary=note_tag_association, back_populates="tags"
    )
