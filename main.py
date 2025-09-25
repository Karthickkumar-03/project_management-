from fastapi import FastAPI
from routers.api_router import api_router
from configurations.database import Base, engine
import models  # Ensure all models imported

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Project Management API")

# Include all API routes
app.include_router(api_router)
