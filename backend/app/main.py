# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# ✅ Updated imports for refactored structure
from app.db.base import Base        # contains all models
from app.db.session import engine    # SQLAlchemy engine
from app.routers import auth, datasets, experiments, results

# -------------------------
# Initialize FastAPI
# -------------------------
#app = FastAPI(title="Regression/Classification App")
from fastapi.responses import ORJSONResponse

app = FastAPI(title="Regression/Classification App", default_response_class=ORJSONResponse)


# -------------------------
# CORS configuration
# -------------------------
origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Create tables
# -------------------------
Base.metadata.create_all(bind=engine)

# -------------------------
# Include routers
# -------------------------
app.include_router(auth.router)
app.include_router(datasets.router)
app.include_router(experiments.router)
app.include_router(results.router)
