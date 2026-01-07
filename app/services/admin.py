from sqlmodel import Session, select
from app.models.soumission import Soumission

def get_soumissions(db: Session, skip: int = 0, limit: int = 20):
    return db.exec(
        select(Soumission)
        .order_by(Soumission.created_at.desc())
        .offset(skip)
        .limit(limit)
    ).all()
