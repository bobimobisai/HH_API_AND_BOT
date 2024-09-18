from typing import List
from fastapi import Depends, Request, APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer
from backend.src.api.v1.function.jwt_function import decrypt_access_token
from backend.src.api.v1.shemas.base_model import (
    Token,
    TokenData,
    CreateUser,
    NoteCreate,
    NoteUpdate,
    TagCreate,
    TagUpdate
)
import uuid
import logging
from backend.db_orm.Models import UserOrm, NoteOrm, TagOrm
from backend.db_orm.CRUD import UserCRUD, NoteCRUD, TagCRUD

logging.basicConfig(level=logging.DEBUG)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

BaseRouter = APIRouter(tags=["API - V1"], prefix="/api/v1")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    email = await decrypt_access_token(token)
    user = await UserCRUD().get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return user


@BaseRouter.post("/notes/", response_model=NoteOrm)
async def create_note(
    note: NoteCreate, current_user: UserOrm = Depends(get_current_user)
):
    return await NoteCRUD.create_note(
        user_id=current_user.id, title=note.title, text=note.text, tags=note.tags
    )


@BaseRouter.get("/notes/{note_id}", response_model=NoteOrm)
async def read_note(
    note_id: uuid.UUID, current_user: UserOrm = Depends(get_current_user)
):
    note = await NoteCRUD.get_note_by_id(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this note"
        )
    return note


@BaseRouter.get("/users/{user_id}/notes", response_model=List[NoteOrm])
async def read_notes_by_user(
    user_id: uuid.UUID, current_user: UserOrm = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access these notes"
        )
    notes = await NoteCRUD.get_notes_by_user(user_id)
    return notes


@BaseRouter.put("/notes/{note_id}", response_model=NoteOrm)
async def update_note(
    note_id: uuid.UUID,
    note: NoteUpdate,
    current_user: UserOrm = Depends(get_current_user),
):
    note_to_update = await NoteCRUD.get_note_by_id(note_id)
    if note_to_update is None:
        raise HTTPException(status_code=404, detail="Note not found")
    if note_to_update.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this note"
        )
    updated_note = await NoteCRUD.update_note(note_id, **note.dict(exclude_unset=True))
    return updated_note


@BaseRouter.delete("/notes/{note_id}")
async def delete_note(
    note_id: uuid.UUID, current_user: UserOrm = Depends(get_current_user)
):
    note_to_delete = await NoteCRUD.get_note_by_id(note_id)
    if note_to_delete is None:
        raise HTTPException(status_code=404, detail="Note not found")
    if note_to_delete.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this note"
        )
    await NoteCRUD.delete_note(note_id)
    return {"detail": "Note deleted"}


@BaseRouter.post("/tags/", response_model=TagOrm)
async def create_tag(tag: TagCreate, current_user: UserOrm = Depends(get_current_user)):
    return await TagCRUD.create_tag(name=tag.name)


@BaseRouter.get("/tags/{tag_id}", response_model=TagOrm)
async def read_tag(
    tag_id: uuid.UUID, current_user: UserOrm = Depends(get_current_user)
):
    tag = await TagCRUD.get_tag_by_id(tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@BaseRouter.get("/tags/", response_model=List[TagOrm])
async def read_tags(current_user: UserOrm = Depends(get_current_user)):
    tags = await TagCRUD.get_all_tags()
    return tags


@BaseRouter.put("/tags/{tag_id}", response_model=TagOrm)
async def update_tag(
    tag_id: uuid.UUID, tag: TagUpdate, current_user: UserOrm = Depends(get_current_user)
):
    updated_tag = await TagCRUD.update_tag(tag_id, **tag.dict())
    if updated_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return updated_tag


@BaseRouter.delete("/tags/{tag_id}")
async def delete_tag(
    tag_id: uuid.UUID, current_user: UserOrm = Depends(get_current_user)
):
    deleted_tag = await TagCRUD.delete_tag(tag_id)
    if deleted_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"detail": "Tag deleted"}
