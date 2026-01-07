from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.soumission import Soumission
from app.schemas.soumission import SoumissionCreate

DUPLICATE_HOURS = 24

def create_soumission(data: SoumissionCreate, db: Session):
    limit = datetime.utcnow() - timedelta(hours=DUPLICATE_HOURS)

    existing = db.exec(
        select(Soumission).where(
            (Soumission.email == data.email) &
            (Soumission.created_at >= limit)
        )
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Demande déjà envoyée récemment"
        )

    soumission = Soumission(**data.dict())
    db.add(soumission)
    db.commit()
    db.refresh(soumission)
    return soumission
