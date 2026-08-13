"""System and integration tests."""

import pytest


class TestHealthCheck:
    """Tests for health check endpoint."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestIntegration:
    """Integration tests for complete workflows."""

    def test_complete_appointment_workflow(self, client):
        """Test complete workflow from creating patient/doctor to appointment."""
        # Create patient
        patient_data = {
            "name": "Alice",
            "email": "alice@example.com",
            "phone": "555-0001"
        }
        patient_response = client.post("/patients", json=patient_data)
        assert patient_response.status_code == 201
        patient_id = patient_response.json()["id"]

        # Create doctor
        doctor_data = {
            "name": "Dr. House",
            "specialization": "Internal Medicine"
        }
        doctor_response = client.post("/doctors", json=doctor_data)
        assert doctor_response.status_code == 201
        doctor_id = doctor_response.json()["id"]

        # Create appointment
        from datetime import datetime, timedelta
        start = (datetime.utcnow() + timedelta(days=1)).replace(microsecond=0)
        end = start + timedelta(hours=1)
        
        appointment_data = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": start.isoformat(),
            "appointment_end": end.isoformat()
        }
        appointment_response = client.post("/appointments", json=appointment_data)
        assert appointment_response.status_code == 201
        appointment_id = appointment_response.json()["id"]

        # Verify appointment has correct details
        get_response = client.get(f"/appointments/{appointment_id}")
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["patient"]["name"] == "Alice"
        assert data["doctor"]["name"] == "Dr. House"

    def test_api_operations_sequence(self, client):
        """Test sequence of API operations."""
        # Get empty lists
        assert client.get("/patients").json() == []
        assert client.get("/doctors").json() == []
        assert client.get("/appointments").json() == []

        # Create multiple patients
        patients = []
        for i in range(3):
            response = client.post("/patients", json={
                "name": f"Patient {i}",
                "email": f"patient{i}@example.com",
                "phone": f"555-000{i}"
            })
            assert response.status_code == 201
            patients.append(response.json())

        # Verify count
        assert len(client.get("/patients").json()) == 3

        # Create doctors
        doctors = []
        for i in range(2):
            response = client.post("/doctors", json={
                "name": f"Dr. Name{i}",
                "specialization": f"Specialty{i}"
            })
            assert response.status_code == 201
            doctors.append(response.json())

        # Verify count
        assert len(client.get("/doctors").json()) == 2

        # Create appointments
        from datetime import datetime, timedelta
        for i in range(4):
            start = (datetime.utcnow() + timedelta(hours=i*2)).replace(microsecond=0)
            end = start + timedelta(hours=1)
            
            response = client.post("/appointments", json={
                "patient_id": patients[i % len(patients)]["id"],
                "doctor_id": doctors[i % len(doctors)]["id"],
                "appointment_start": start.isoformat(),
                "appointment_end": end.isoformat()
            })
            assert response.status_code == 201

        # Verify count
        assert len(client.get("/appointments").json()) == 4
