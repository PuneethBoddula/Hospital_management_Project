"""Main FastAPI application."""

import os

from fastapi import FastAPI

from hospital_management_project.database import Base, engine
from hospital_management_project.routers import (
    appointment_router,
    doctor_router,
    patient_router,
)

# Create tables only if not running tests
if not os.environ.get("TESTING"):
    Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Hospital Appointment Management API",
    description="API for managing hospital patients, doctors, and appointments",
    version="0.1.0"
)

# Include routers
app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(appointment_router)


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    # Get host from environment variable, default to 0.0.0.0 for Docker
    host = os.environ.get("HOST", "0.0.0.0")  # nosec B104
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
