from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.services import registry as svc

router = APIRouter()
templates = Jinja2Templates(directory="backend/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, card_id: str | None = None, db: AsyncSession = Depends(get_db)):
    cards = await svc.list_cards(db)
    cid = card_id or (cards[0].id if cards else None)
    vers = await svc.versions(db, cid) if cid else []
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Model Registry Board", "cards": cards, "card_id": cid, "versions": vers},
    )

@router.post("/ui/cards")
async def ui_card(name: str = Form(...), description: str = Form(""), db: AsyncSession = Depends(get_db)):
    c = await svc.create_card(db, name, description)
    return RedirectResponse(f"/?card_id={c.id}", status_code=303)

@router.post("/ui/versions")
async def ui_ver(
    card_id: str = Form(...),
    version: str = Form(...),
    artifact_uri: str = Form("s3://models/demo"),
    db: AsyncSession = Depends(get_db),
):
    await svc.register_version(db, card_id, version, artifact_uri)
    return RedirectResponse(f"/?card_id={card_id}", status_code=303)

@router.post("/ui/promote")
async def ui_promote(version_id: str = Form(...), card_id: str = Form(...), db: AsyncSession = Depends(get_db)):
    await svc.promote(db, version_id)
    return RedirectResponse(f"/?card_id={card_id}", status_code=303)

@router.post("/ui/demote")
async def ui_demote(version_id: str = Form(...), card_id: str = Form(...), db: AsyncSession = Depends(get_db)):
    await svc.demote(db, version_id)
    return RedirectResponse(f"/?card_id={card_id}", status_code=303)
