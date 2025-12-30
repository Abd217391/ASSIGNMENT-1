from fastapi import FastAPI
from app.database import engine
from app.models import user
from app.routers import auth

user.Base.metadata.create_all(bind=engine)



app = FastAPI(title="INSTAGRAM PORTAL")

app.include_router(auth.router)
