from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_db
from app.schemas.soumission import SoumissionCreate, SoumissionOut
from app.services.soumission import create_soumission
from app.utils.rate_limit import RateLimiter

router = APIRouter(prefix="/soumissions", tags=["Soumissions"])
rate_limit = RateLimiter(3, 60)

@router.post("/", response_model=SoumissionOut,
             dependencies=[Depends(rate_limit)])
def envoyer(data: SoumissionCreate, db: Session = Depends(get_db)):
    return create_soumission(data, db)
