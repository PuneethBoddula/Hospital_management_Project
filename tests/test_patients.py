"""Tests for patient API endpoints."""



class TestPatientAPI:
    """Tests for Patient API endpoints."""

    def test_get_all_patients_empty(self, client):
        """Test retrieving patients when none exist."""
        response = client.get("/patients")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_patients_with_data(self, client, sample_patient):
        """Test retrieving all patients."""
        response = client.get("/patients")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "John Doe"
        assert data[0]["email"] == "john@example.com"

    def test_create_patient_success(self, client):
        """Test successful patient creation."""
        patient_data = {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "phone": "555-5678"
        }
        response = client.post("/patients", json=patient_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Jane Smith"
        assert data["email"] == "jane@example.com"
        assert data["phone"] == "555-5678"
        assert "id" in data

    def test_create_patient_duplicate_email(self, client, sample_patient):
        """Test patient creation with duplicate email."""
        patient_data = {
            "name": "Another Person",
            "email": "john@example.com",
            "phone": "555-9999"
        }
        response = client.post("/patients", json=patient_data)
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_create_patient_invalid_email(self, client):
        """Test patient creation with invalid email."""
        patient_data = {
            "name": "Invalid Email",
            "email": "not-an-email",
            "phone": "555-1234"
        }
        response = client.post("/patients", json=patient_data)
        assert response.status_code == 422

    def test_get_patient_by_id_success(self, client, sample_patient):
        """Test retrieving patient by ID."""
        response = client.get(f"/patients/{sample_patient.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_patient.id
        assert data["name"] == "John Doe"

    def test_get_patient_by_id_not_found(self, client):
        """Test retrieving non-existent patient."""
        response = client.get("/patients/999")
        assert response.status_code == 404
        assert "Patient not found" in response.json()["detail"]

    def test_get_patient_with_appointments(self, client, sample_patient, sample_appointment):
        """Test retrieving patient with appointments."""
        response = client.get(f"/patients/{sample_patient.id}")
        assert response.status_code == 200
        data = response.json()
        assert "appointments" in data
        assert len(data["appointments"]) == 1
        assert data["appointments"][0]["id"] == sample_appointment.id
