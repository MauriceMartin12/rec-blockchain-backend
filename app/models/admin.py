from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Admin(SQLModel, table=True):
    __tablename__ = "admin"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str

    is_admin: bool = Field(default=False)
    is_active: bool = Field(default=True)  # <- Ajouté ici

    created_at: datetime = Field(default_factory=datetime.utcnow)
