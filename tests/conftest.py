"""Test configuration and fixtures."""

import os
from datetime import UTC, datetime, timedelta

import pytest

# Set testing mode before importing anything else
os.environ["TESTING"] = "1"

# Now import the models and database from the project
from fastapi.testclient import TestClient

from hospital_management_project.database import Base, SessionLocal, engine, get_db
from app.main import app
from hospital_management_project.models import (
    Appointment,
    Doctor,
    Patient,
)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    session = SessionLocal()
    yield session
    session.close()
    # Clean up after test
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with the test database."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_patient(db_session):
    """Create a sample patient for testing."""
    patient = Patient(
        name="John Doe",
        email="john@example.com",
        phone="555-1234"
    )
    db_session.add(patient)
    db_session.commit()
    db_session.refresh(patient)
    return patient


@pytest.fixture
def sample_doctor(db_session):
    """Create a sample doctor for testing."""
    doctor = Doctor(
        name="Dr. Smith",
        specialization="Cardiology"
    )
    db_session.add(doctor)
    db_session.commit()
    db_session.refresh(doctor)
    return doctor


@pytest.fixture
def sample_appointment(db_session, sample_patient, sample_doctor):
    """Create a sample appointment for testing."""
    start = datetime.now(UTC).replace(microsecond=0)
    end = start + timedelta(hours=1)
    
    appointment = Appointment(
        patient_id=sample_patient.id,
        doctor_id=sample_doctor.id,
        appointment_start=start,
        appointment_end=end
    )
    db_session.add(appointment)
    db_session.commit()
    db_session.refresh(appointment)
    return appointment
