"""Tests for appointment API endpoints."""

from datetime import datetime, timedelta
import pytest


class TestAppointmentAPI:
    """Tests for Appointment API endpoints."""

    def test_get_all_appointments_empty(self, client):
        """Test retrieving appointments when none exist."""
        response = client.get("/appointments")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_appointments_with_data(self, client, sample_appointment):
        """Test retrieving all appointments."""
        response = client.get("/appointments")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["patient_id"] == sample_appointment.patient_id

    def test_create_appointment_success(self, client, sample_patient, sample_doctor):
        """Test successful appointment creation."""
        start = (datetime.utcnow() + timedelta(days=1)).replace(microsecond=0)
        end = start + timedelta(hours=1)
        
        appointment_data = {
            "patient_id": sample_patient.id,
            "doctor_id": sample_doctor.id,
            "appointment_start": start.isoformat(),
            "appointment_end": end.isoformat()
        }
        response = client.post("/appointments", json=appointment_data)
        assert response.status_code == 201
        data = response.json()
        assert data["patient_id"] == sample_patient.id
        assert data["doctor_id"] == sample_doctor.id
        assert "id" in data

    def test_create_appointment_nonexistent_patient(self, client, sample_doctor):
        """Test appointment creation with non-existent patient."""
        start = (datetime.utcnow() + timedelta(days=1)).replace(microsecond=0)
        end = start + timedelta(hours=1)
        
        appointment_data = {
            "patient_id": 999,
            "doctor_id": sample_doctor.id,
            "appointment_start": start.isoformat(),
            "appointment_end": end.isoformat()
        }
        response = client.post("/appointments", json=appointment_data)
        assert response.status_code == 404
        assert "Patient not found" in response.json()["detail"]

    def test_create_appointment_nonexistent_doctor(self, client, sample_patient):
        """Test appointment creation with non-existent doctor."""
        start = (datetime.utcnow() + timedelta(days=1)).replace(microsecond=0)
        end = start + timedelta(hours=1)
        
        appointment_data = {
            "patient_id": sample_patient.id,
            "doctor_id": 999,
            "appointment_start": start.isoformat(),
            "appointment_end": end.isoformat()
        }
        response = client.post("/appointments", json=appointment_data)
        assert response.status_code == 404
        assert "Doctor not found" in response.json()["detail"]

    def test_create_appointment_invalid_times(self, client, sample_patient, sample_doctor):
        """Test appointment creation with invalid time range."""
        start = (datetime.utcnow() + timedelta(days=1)).replace(microsecond=0)
        end = start - timedelta(hours=1)  # End before start
        
        appointment_data = {
            "patient_id": sample_patient.id,
            "doctor_id": sample_doctor.id,
            "appointment_start": start.isoformat(),
            "appointment_end": end.isoformat()
        }
        response = client.post("/appointments", json=appointment_data)
        assert response.status_code == 400
        assert "start time must be before end time" in response.json()["detail"]

    def test_get_appointment_by_id_success(self, client, sample_appointment):
        """Test retrieving appointment by ID."""
        response = client.get(f"/appointments/{sample_appointment.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_appointment.id
        assert data["patient_id"] == sample_appointment.patient_id

    def test_get_appointment_by_id_not_found(self, client):
        """Test retrieving non-existent appointment."""
        response = client.get("/appointments/999")
        assert response.status_code == 404
        assert "Appointment not found" in response.json()["detail"]

    def test_get_appointment_with_details(self, client, sample_appointment):
        """Test retrieving appointment with patient and doctor details."""
        response = client.get(f"/appointments/{sample_appointment.id}")
        assert response.status_code == 200
        data = response.json()
        assert "patient" in data
        assert "doctor" in data
        assert data["patient"]["name"] == "John Doe"
        assert data["doctor"]["name"] == "Dr. Smith"


class TestAppointmentOverlap:
    """Tests for appointment overlap prevention."""

    def test_no_overlap_consecutive_appointments(self, client, sample_patient, sample_doctor, sample_appointment):
        """Test that consecutive appointments are allowed."""
        # Sample appointment: 10:00-11:00
        # New appointment: 11:00-12:00 (should be allowed)
        start = sample_appointment.appointment_end
        end = start + timedelta(hours=1)
        
        appointment_data = {
            "patient_id": sample_patient.id,
            "doctor_id": sample_doctor.id,
            "appointment_start": start.isoformat(),
            "appointment_end": end.isoformat()
        }
        response = client.post("/appointments", json=appointment_data)
        assert response.status_code == 201

    def test_overlap_during_appointment(self, client, sample_patient, sample_doctor, sample_appointment):
        """Test that overlapping appointments are rejected."""
        # Sample appointment: 10:00-11:00
        # New appointment: 10:30-11:30 (overlaps)
        start = sample_appointment.appointment_start + timedelta(minutes=30)
        end = start + timedelta(hours=1)
        
        appointment_data = {
            "patient_id": sample_patient.id,
            "doctor_id": sample_doctor.id,
            "appointment_start": start.isoformat(),
            "appointment_end": end.isoformat()
        }
        response = client.post("/appointments", json=appointment_data)
        assert response.status_code == 409
        assert "overlaps with an existing appointment" in response.json()["detail"]

    def test_overlap_within_appointment(self, client, sample_patient, sample_doctor, sample_appointment):
        """Test that appointments fully within existing appointment are rejected."""
        # Sample appointment: 10:00-11:00
        # New appointment: 10:15-10:45 (within)
        start = sample_appointment.appointment_start + timedelta(minutes=15)
        end = start + timedelta(minutes=30)
        
        appointment_data = {
            "patient_id": sample_patient.id,
            "doctor_id": sample_doctor.id,
            "appointment_start": start.isoformat(),
            "appointment_end": end.isoformat()
        }
        response = client.post("/appointments", json=appointment_data)
        assert response.status_code == 409
        assert "overlaps with an existing appointment" in response.json()["detail"]

    def test_overlap_starting_before_ending_after(self, client, sample_patient, sample_doctor, sample_appointment):
        """Test that appointments overlapping before and after are rejected."""
        # Sample appointment: 10:00-11:00
        # New appointment: 09:30-11:30 (starts before and ends after)
        start = sample_appointment.appointment_start - timedelta(minutes=30)
        end = sample_appointment.appointment_end + timedelta(minutes=30)
        
        appointment_data = {
            "patient_id": sample_patient.id,
            "doctor_id": sample_doctor.id,
            "appointment_start": start.isoformat(),
            "appointment_end": end.isoformat()
        }
        response = client.post("/appointments", json=appointment_data)
        assert response.status_code == 409

    def test_overlap_different_doctor(self, client, db_session, sample_patient, sample_appointment):
        """Test that appointments for different doctors don't conflict."""
        # Create a different doctor
        from hospital_management_project.models import Doctor
        doctor2 = Doctor(name="Dr. Jones", specialization="Pediatrics")
        db_session.add(doctor2)
        db_session.commit()
        db_session.refresh(doctor2)
        
        # Create overlapping appointment with different doctor
        start = sample_appointment.appointment_start + timedelta(minutes=30)
        end = start + timedelta(hours=1)
        
        appointment_data = {
            "patient_id": sample_patient.id,
            "doctor_id": doctor2.id,
            "appointment_start": start.isoformat(),
            "appointment_end": end.isoformat()
        }
        
        response = client.post("/appointments", json=appointment_data)
        # Should succeed because it's a different doctor
        assert response.status_code == 201

    def test_multiple_non_overlapping_appointments(self, client, sample_patient, sample_doctor):
        """Test creating multiple non-overlapping appointments for same doctor."""
        appointments = [
            {
                "patient_id": sample_patient.id,
                "doctor_id": sample_doctor.id,
                "appointment_start": (datetime.utcnow() + timedelta(hours=1)).replace(microsecond=0).isoformat(),
                "appointment_end": (datetime.utcnow() + timedelta(hours=2)).replace(microsecond=0).isoformat(),
            },
            {
                "patient_id": sample_patient.id,
                "doctor_id": sample_doctor.id,
                "appointment_start": (datetime.utcnow() + timedelta(hours=3)).replace(microsecond=0).isoformat(),
                "appointment_end": (datetime.utcnow() + timedelta(hours=4)).replace(microsecond=0).isoformat(),
            },
        ]
        
        for appointment_data in appointments:
            response = client.post("/appointments", json=appointment_data)
            assert response.status_code == 201
        
        response = client.get("/appointments")
        assert len(response.json()) == 2
