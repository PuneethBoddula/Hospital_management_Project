"""Tests for doctor API endpoints."""

import pytest


class TestDoctorAPI:
    """Tests for Doctor API endpoints."""

    def test_get_all_doctors_empty(self, client):
        """Test retrieving doctors when none exist."""
        response = client.get("/doctors")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_doctors_with_data(self, client, sample_doctor):
        """Test retrieving all doctors."""
        response = client.get("/doctors")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Dr. Smith"
        assert data[0]["specialization"] == "Cardiology"

    def test_create_doctor_success(self, client):
        """Test successful doctor creation."""
        doctor_data = {
            "name": "Dr. Johnson",
            "specialization": "Neurology"
        }
        response = client.post("/doctors", json=doctor_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Dr. Johnson"
        assert data["specialization"] == "Neurology"
        assert "id" in data

    def test_create_doctor_missing_fields(self, client):
        """Test doctor creation with missing fields."""
        doctor_data = {
            "name": "Dr. Incomplete"
        }
        response = client.post("/doctors", json=doctor_data)
        assert response.status_code == 422

    def test_get_doctor_by_id_success(self, client, sample_doctor):
        """Test retrieving doctor by ID."""
        response = client.get(f"/doctors/{sample_doctor.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_doctor.id
        assert data["name"] == "Dr. Smith"

    def test_get_doctor_by_id_not_found(self, client):
        """Test retrieving non-existent doctor."""
        response = client.get("/doctors/999")
        assert response.status_code == 404
        assert "Doctor not found" in response.json()["detail"]

    def test_get_doctor_with_appointments(self, client, sample_doctor, sample_appointment):
        """Test retrieving doctor with appointments."""
        response = client.get(f"/doctors/{sample_doctor.id}")
        assert response.status_code == 200
        data = response.json()
        assert "appointments" in data
        assert len(data["appointments"]) == 1
        assert data["appointments"][0]["id"] == sample_appointment.id

    def test_multiple_doctors_creation(self, client):
        """Test creating multiple doctors."""
        doctors = [
            {"name": "Dr. A", "specialization": "Cardiology"},
            {"name": "Dr. B", "specialization": "Neurology"},
            {"name": "Dr. C", "specialization": "Dermatology"},
        ]
        
        for doctor_data in doctors:
            response = client.post("/doctors", json=doctor_data)
            assert response.status_code == 201
        
        response = client.get("/doctors")
        assert response.status_code == 200
        assert len(response.json()) == 3
