"""Test configuration and fixtures."""

import os
import pytest
from datetime import datetime, timedelta

# Set testing mode before importing anything else
os.environ["TESTING"] = "1"

# Now import the models and database from the project
from hospital_management_project.database import Base, get_db, engine, SessionLocal
from hospital_management_project.models import Patient, Doctor, Appointment  # noqa: F401
from hospital_management_project.main import app
from fastapi.testclient import TestClient


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
    start = datetime.utcnow().replace(microsecond=0)
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
