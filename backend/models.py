from __future__ import annotations
from datetime import datetime
from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from backend.db import Base

def utcnow(): return datetime.utcnow()

class ModelCard(Base):
    __tablename__ = "model_cards"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, default="")
    owner: Mapped[str] = mapped_column(String(80), default="ml-team")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)

class ModelVersion(Base):
    __tablename__ = "model_versions"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    card_id: Mapped[str] = mapped_column(String(32), index=True)
    version: Mapped[str] = mapped_column(String(40))
    stage: Mapped[str] = mapped_column(String(24), default="staging", index=True)
    artifact_uri: Mapped[str] = mapped_column(String(300), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
