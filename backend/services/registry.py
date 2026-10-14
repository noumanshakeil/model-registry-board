from __future__ import annotations
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models import ModelCard, ModelVersion

async def create_card(session: AsyncSession, name: str, description: str = "", owner: str = "ml-team") -> ModelCard:
    row = ModelCard(
        id=uuid.uuid4().hex[:10],
        name=name.strip()[:120],
        description=description.strip(),
        owner=owner.strip()[:80],
    )
    session.add(row)
    await session.commit()
    await session.refresh(row)
    return row

async def list_cards(session: AsyncSession) -> list[ModelCard]:
    return list((await session.execute(select(ModelCard).order_by(ModelCard.created_at.desc()))).scalars())

async def register_version(
    session: AsyncSession, card_id: str, version: str, artifact_uri: str = "", stage: str = "staging"
) -> ModelVersion:
    stage = stage if stage in {"staging", "prod"} else "staging"
    row = ModelVersion(
        id=uuid.uuid4().hex[:12],
        card_id=card_id,
        version=version.strip()[:40],
        stage=stage,
        artifact_uri=artifact_uri.strip()[:300],
    )
    session.add(row)
    await session.commit()
    await session.refresh(row)
    return row

async def versions(session: AsyncSession, card_id: str) -> list[ModelVersion]:
    return list(
        (
            await session.execute(
                select(ModelVersion)
                .where(ModelVersion.card_id == card_id)
                .order_by(ModelVersion.created_at.desc())
            )
        ).scalars()
    )

async def promote(session: AsyncSession, version_id: str) -> ModelVersion:
    row = await session.get(ModelVersion, version_id)
    if not row:
        raise ValueError("not found")
    row.stage = "prod"
    await session.commit()
    await session.refresh(row)
    return row

async def demote(session: AsyncSession, version_id: str) -> ModelVersion:
    row = await session.get(ModelVersion, version_id)
    if not row:
        raise ValueError("not found")
    row.stage = "staging"
    await session.commit()
    await session.refresh(row)
    return row
