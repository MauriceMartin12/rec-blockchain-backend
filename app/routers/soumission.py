from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_db
from schemas.soumission import SoumissionCreate, SoumissionOut
from services.soumission import create_soumission
from utils.rate_limit import RateLimiter

router = APIRouter(prefix="/soumissions", tags=["Soumissions"])
rate_limit = RateLimiter(3, 60)

@router.post("/", response_model=SoumissionOut,
             dependencies=[Depends(rate_limit)])
def envoyer(data: SoumissionCreate, db: Session = Depends(get_db)):
    return create_soumission(data, db)
