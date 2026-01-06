from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import soumission, admin
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Application Web Professionnelle",
    version="1.0.0"
)

app.include_router(soumission.router)
app.include_router(admin.router)
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.get("/")
async def root():
    return {"message": "Bienvenue dans rec_blockchain"}


@app.on_event("startup")
def startup():
    create_db_and_tables()
