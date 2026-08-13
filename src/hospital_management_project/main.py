"""Main FastAPI application."""

import os
from fastapi import FastAPI
from hospital_management_project.routers import patient_router, doctor_router, appointment_router
from hospital_management_project.database import Base, engine

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
    uvicorn.run(app, host="0.0.0.0", port=8000)
