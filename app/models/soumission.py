from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import EmailStr
from datetime import datetime

class Soumission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    prenom: str
    email: EmailStr
    telephone: str
    adresse: str
    besoin: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
