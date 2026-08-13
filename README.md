# Hospital Appointment Management API

A FastAPI-based REST API for managing hospital patients, doctors, and appointments with database persistence and comprehensive testing.

## Features

- **Patient Management**: Create and retrieve patient information
- **Doctor Management**: Manage doctors and their specializations
- **Appointment Management**: Schedule appointments with automatic conflict detection
- **Overlap Prevention**: Prevents overlapping appointments for the same doctor
- **Database Migrations**: Alembic-based schema management
- **Comprehensive Testing**: 85%+ test coverage with pytest
- **Security**: Bandit security scanning in CI/CD
- **Docker Support**: Containerized deployment with health checks
- **CI/CD Pipeline**: GitHub Actions workflow for automated testing and deployment

## Technology Stack

- **Framework**: FastAPI 0.141.1
- **Server**: Uvicorn 0.52.2
- **Database**: SQLAlchemy 2.0.52 with SQLite
- **Migrations**: Alembic 1.19.1
- **Validation**: Pydantic 2.13.4
- **Testing**: Pytest 9.1.1
- **Security**: Bandit 1.9.4
- **Code Quality**: Ruff 0.16.2

## Project Structure

```
hospital-management-project/
├── src/
│   └── hospital_management_project/
│       ├── __init__.py
│       ├── main.py
│       ├── database.py
│       ├── models/
│       │   ├── patient.py
│       │   ├── doctor.py
│       │   └── appointment.py
│       ├── schemas/
│       │   └── __init__.py
│       ├── routers/
│       │   └── __init__.py
│       └── services/
│           └── __init__.py
├── tests/
│   ├── conftest.py
│   ├── test_patients.py
│   ├── test_doctors.py
│   ├── test_appointments.py
│   └── test_integration.py
├── alembic/
├── .github/workflows/
│   └── ci-cd.yml
├── Dockerfile
├── pyproject.toml
└── README.md
```

## Installation

### Prerequisites

- Python 3.14+
- pip or poetry

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/hospital-management-project.git
cd hospital-management-project
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
# or
pip install -r requirements.txt
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the development server:
```bash
uvicorn hospital_management_project.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Patients
- `GET /patients` - Retrieve all patients
- `POST /patients` - Create a new patient
- `GET /patients/{id}` - Retrieve a patient by ID

### Doctors
- `GET /doctors` - Retrieve all doctors
- `POST /doctors` - Create a new doctor
- `GET /doctors/{id}` - Retrieve a doctor by ID

### Appointments
- `GET /appointments` - Retrieve all appointments
- `POST /appointments` - Create a new appointment
- `GET /appointments/{id}` - Retrieve an appointment by ID

### Health
- `GET /health` - Health check endpoint

## Example Usage

### Create a Patient
```bash
curl -X POST http://localhost:8000/patients \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "555-1234"
  }'
```

### Create a Doctor
```bash
curl -X POST http://localhost:8000/doctors \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Smith",
    "specialization": "Cardiology"
  }'
```

### Create an Appointment
```bash
curl -X POST http://localhost:8000/appointments \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "doctor_id": 1,
    "appointment_start": "2024-12-15T10:00:00",
    "appointment_end": "2024-12-15T11:00:00"
  }'
```

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=src/hospital_management_project --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html
```

## Docker

Build the Docker image:
```bash
docker build -t hospital-appointment-management:latest .
```

Run the container:
```bash
docker run -d -p 8000:8000 --name hospital-api hospital-appointment-management:latest
```

The API will be available at `http://localhost:8000`

## CI/CD Pipeline

The GitHub Actions workflow automatically:
1. **Lints** code using Ruff
2. **Tests** with pytest (minimum 85% coverage required)
3. **Scans** for security issues with Bandit
4. **Builds** and publishes Docker image to Docker Hub

### Setting up Docker Hub Deployment

1. Create a Docker Hub account
2. Add GitHub Secrets to your repository:
   - `DOCKERHUB_USERNAME`: Your Docker Hub username
   - `DOCKERHUB_TOKEN`: A Docker Hub access token

3. Merge/push to `main` branch to trigger the workflow

The image-publish job runs on pushes to `main`. If either secret is missing, its
login and publish steps are skipped; configure both secrets before submitting.

## Database

The application uses SQLite for development and can be configured to use PostgreSQL for production.

### Running Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Revert migrations
alembic downgrade -1
```

## Business Rules

### Appointment Overlap Prevention
The system prevents overlapping appointments for the same doctor. An appointment cannot be created if its time range overlaps with an existing appointment for the same doctor.

Overlap condition: `existing_start < new_end AND existing_end > new_start`

## Security

- Bandit security scanning for code vulnerabilities
- Input validation using Pydantic
- Foreign key constraints for data integrity
- Non-root user in Docker container
- Health checks for container monitoring

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting
4. Submit a pull request

## License

MIT License

## Support

For issues and questions, please use the GitHub Issues page.
