from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from database import get_db
from schemas.admin import AdminLogin, Token
from services.admin import get_soumissions
from services.admin import get_soumissions
from core.security import create_access_token, verify_password
from core.dependencies import get_current_admin
from models.admin import Admin

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/login", response_model=Token)
def login(data: AdminLogin, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.username == data.username).first()
    if not admin or not verify_password(data.password, admin.hashed_password):
        raise HTTPException(status_code=401)

    token = create_access_token({"sub": admin.username})
    return {"access_token": token}

@router.get("/soumissions")
def dashboard(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return get_soumissions(db)
