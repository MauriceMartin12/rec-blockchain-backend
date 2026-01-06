from pydantic import BaseModel, EmailStr
from datetime import datetime

class SoumissionCreate(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    telephone: str
    adresse: str
    besoin: str

class SoumissionOut(SoumissionCreate):
    id: int
    created_at: datetime
