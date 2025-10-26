from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn
from typing import List, Optional
import os

from app.config import settings
from app.routers import documents, content, templates, auth

# Initialize FastAPI app
app = FastAPI(
    title="Crater API",
    description="Knowledge Management + RAG-Powered Content Creation Platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
app.include_router(content.router, prefix="/api/content", tags=["content"])
app.include_router(templates.router, prefix="/api/templates", tags=["templates"])

@app.get("/")
async def root():
    return {"message": "Crater API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
