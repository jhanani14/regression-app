from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from backend.db import Base, engine
from backend.routers import datasets, experiments
from backend import auth

app = FastAPI()

origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(datasets.router)
app.include_router(experiments.router)
