"""API routers for patients, doctors, and appointments."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from hospital_management_project.database import get_db
from hospital_management_project.schemas import (
    PatientCreate, PatientResponse, PatientWithAppointments,
    DoctorCreate, DoctorResponse, DoctorWithAppointments,
    AppointmentCreate, AppointmentResponse, AppointmentWithDetails
)
from hospital_management_project.services import (
    PatientService, DoctorService, AppointmentService
)

# Create routers
patient_router = APIRouter(prefix="/patients", tags=["patients"])
doctor_router = APIRouter(prefix="/doctors", tags=["doctors"])
appointment_router = APIRouter(prefix="/appointments", tags=["appointments"])


# Patient endpoints
@patient_router.get("", response_model=list[PatientResponse], status_code=status.HTTP_200_OK)
def get_all_patients(db: Session = Depends(get_db)):
    """Retrieve all patients."""
    return PatientService.get_all_patients(db)


@patient_router.post("", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    """Create a new patient."""
    return PatientService.create_patient(patient, db)


@patient_router.get("/{patient_id}", response_model=PatientWithAppointments, status_code=status.HTTP_200_OK)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    """Retrieve a patient by ID."""
    return PatientService.get_patient_by_id(patient_id, db)


# Doctor endpoints
@doctor_router.get("", response_model=list[DoctorResponse], status_code=status.HTTP_200_OK)
def get_all_doctors(db: Session = Depends(get_db)):
    """Retrieve all doctors."""
    return DoctorService.get_all_doctors(db)


@doctor_router.post("", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    """Create a new doctor."""
    return DoctorService.create_doctor(doctor, db)


@doctor_router.get("/{doctor_id}", response_model=DoctorWithAppointments, status_code=status.HTTP_200_OK)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """Retrieve a doctor by ID."""
    return DoctorService.get_doctor_by_id(doctor_id, db)


# Appointment endpoints
@appointment_router.get("", response_model=list[AppointmentResponse], status_code=status.HTTP_200_OK)
def get_all_appointments(db: Session = Depends(get_db)):
    """Retrieve all appointments."""
    return AppointmentService.get_all_appointments(db)


@appointment_router.post("", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    """Create a new appointment."""
    return AppointmentService.create_appointment(appointment, db)


@appointment_router.get("/{appointment_id}", response_model=AppointmentWithDetails, status_code=status.HTTP_200_OK)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """Retrieve an appointment by ID."""
    return AppointmentService.get_appointment_by_id(appointment_id, db)
