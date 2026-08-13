"""Service layer for business logic."""

from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session

from hospital_management_project.models import Appointment, Doctor, Patient


class PatientService:
    """Service for patient operations."""

    @staticmethod
    def get_all_patients(db: Session):
        """Get all patients."""
        return db.query(Patient).all()

    @staticmethod
    def get_patient_by_id(patient_id: int, db: Session):
        """Get patient by ID."""
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
        return patient

    @staticmethod
    def create_patient(patient_data, db: Session):
        """Create a new patient."""
        # Check if email already exists
        existing_patient = db.query(Patient).filter(Patient.email == patient_data.email).first()
        if existing_patient:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        db_patient = Patient(
            name=patient_data.name,
            email=patient_data.email,
            phone=patient_data.phone
        )
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)
        return db_patient


class DoctorService:
    """Service for doctor operations."""

    @staticmethod
    def get_all_doctors(db: Session):
        """Get all doctors."""
        return db.query(Doctor).all()

    @staticmethod
    def get_doctor_by_id(doctor_id: int, db: Session):
        """Get doctor by ID."""
        doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found"
            )
        return doctor

    @staticmethod
    def create_doctor(doctor_data, db: Session):
        """Create a new doctor."""
        db_doctor = Doctor(
            name=doctor_data.name,
            specialization=doctor_data.specialization
        )
        db.add(db_doctor)
        db.commit()
        db.refresh(db_doctor)
        return db_doctor


class AppointmentService:
    """Service for appointment operations."""

    @staticmethod
    def check_appointment_overlap(
        doctor_id: int,
        appointment_start: datetime,
        appointment_end: datetime,
        db: Session,
        exclude_appointment_id: int | None = None,
    ) -> bool:
        """
        Check if a new appointment overlaps with existing appointments for the same doctor.

        Returns True if there is an overlap, False otherwise.

        The overlap condition is:
        existing_start < new_end AND existing_end > new_start
        """
        query = db.query(Appointment).filter(
            and_(
                Appointment.doctor_id == doctor_id,
                Appointment.appointment_start < appointment_end,
                Appointment.appointment_end > appointment_start
            )
        )

        if exclude_appointment_id:
            query = query.filter(Appointment.id != exclude_appointment_id)

        return query.first() is not None

    @staticmethod
    def get_all_appointments(db: Session):
        """Get all appointments."""
        return db.query(Appointment).all()

    @staticmethod
    def get_appointment_by_id(appointment_id: int, db: Session):
        """Get appointment by ID."""
        appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found"
            )
        return appointment

    @staticmethod
    def create_appointment(appointment_data, db: Session):
        """Create a new appointment."""
        # Validate that patient exists
        patient = db.query(Patient).filter(Patient.id == appointment_data.patient_id).first()
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )

        # Validate that doctor exists
        doctor = db.query(Doctor).filter(Doctor.id == appointment_data.doctor_id).first()
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found"
            )

        # Validate appointment times
        if appointment_data.appointment_start >= appointment_data.appointment_end:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Appointment start time must be before end time"
            )

        # Check for overlapping appointments
        if AppointmentService.check_appointment_overlap(
            appointment_data.doctor_id,
            appointment_data.appointment_start,
            appointment_data.appointment_end,
            db
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This time slot overlaps with an existing appointment for this doctor"
            )

        db_appointment = Appointment(
            patient_id=appointment_data.patient_id,
            doctor_id=appointment_data.doctor_id,
            appointment_start=appointment_data.appointment_start,
            appointment_end=appointment_data.appointment_end
        )
        db.add(db_appointment)
        db.commit()
        db.refresh(db_appointment)
        return db_appointment
