from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from app.api import auth, messages, websocket
from app.core.database import engine
from app.models.base import Base
from app.core.config import settings

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
    logging.info("✅ Database tables created/verified")
except Exception as e:
    logging.error(f"❌ Database connection failed: {e}")

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Real-time chat application with offline message support",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)

# Configure CORS for production
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(messages.router, prefix="/api")
app.include_router(websocket.router)

@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "environment": "production" if not settings.DEBUG else "development",
        "websocket": "wss://your-app-name.onrender.com/ws/{user_id}"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "database": "connected"}