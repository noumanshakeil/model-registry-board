from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.services import registry as svc

class CardIn(BaseModel):
    name: str = Field(min_length=2)
    description: str = ""
    owner: str = "ml-team"

class VersionIn(BaseModel):
    version: str = Field(min_length=1)
    artifact_uri: str = ""
    stage: str = "staging"

router = APIRouter()

@router.get("/cards")
async def cards(db: AsyncSession = Depends(get_db)):
    rows = await svc.list_cards(db)
    return {"cards": [{"id": c.id, "name": c.name, "owner": c.owner, "description": c.description[:200]} for c in rows]}

@router.post("/cards")
async def create_card(payload: CardIn, db: AsyncSession = Depends(get_db)):
    c = await svc.create_card(db, payload.name, payload.description, payload.owner)
    return {"id": c.id, "name": c.name}

@router.post("/cards/{card_id}/versions")
async def add_version(card_id: str, payload: VersionIn, db: AsyncSession = Depends(get_db)):
    v = await svc.register_version(db, card_id, payload.version, payload.artifact_uri, payload.stage)
    return {"id": v.id, "stage": v.stage}

@router.get("/cards/{card_id}/versions")
async def list_versions(card_id: str, db: AsyncSession = Depends(get_db)):
    rows = await svc.versions(db, card_id)
    return {
        "versions": [
            {"id": v.id, "version": v.version, "stage": v.stage, "artifact_uri": v.artifact_uri}
            for v in rows
        ]
    }

@router.post("/versions/{version_id}/promote")
async def promote(version_id: str, db: AsyncSession = Depends(get_db)):
    try:
        v = await svc.promote(db, version_id)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc
    return {"id": v.id, "stage": v.stage}

@router.post("/versions/{version_id}/demote")
async def demote(version_id: str, db: AsyncSession = Depends(get_db)):
    try:
        v = await svc.demote(db, version_id)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc
    return {"id": v.id, "stage": v.stage}
