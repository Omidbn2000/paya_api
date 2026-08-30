from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, patients
from fastapi.middleware.cors import CORSMiddleware
import os

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Patient House Management API",
    description="A simple API for managing patient houses with authentication",
    version="1.0.0"
)

# Allow all origins (for testing/development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(patients.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Patient House Management API",
        "docs": "/docs",
        "endpoints": {
            "signup": "/auth/signup",
            "login": "/auth/login",
            "patient_houses": "/patients"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}