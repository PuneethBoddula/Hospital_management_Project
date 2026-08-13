"""Pydantic schemas for request/response validation."""

from datetime import datetime

from pydantic import BaseModel, EmailStr


# Patient Schemas
class PatientBase(BaseModel):
    """Base patient schema."""

    name: str
    email: EmailStr
    phone: str


class PatientCreate(PatientBase):
    """Patient creation schema."""


class PatientResponse(PatientBase):
    """Patient response schema."""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PatientWithAppointments(PatientResponse):
    """Patient response with appointments."""

    appointments: list[AppointmentResponse] = []


# Doctor Schemas
class DoctorBase(BaseModel):
    """Base doctor schema."""

    name: str
    specialization: str


class DoctorCreate(DoctorBase):
    """Doctor creation schema."""


class DoctorResponse(DoctorBase):
    """Doctor response schema."""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class DoctorWithAppointments(DoctorResponse):
    """Doctor response with appointments."""

    appointments: list[AppointmentResponse] = []


# Appointment Schemas
class AppointmentBase(BaseModel):
    """Base appointment schema."""

    patient_id: int
    doctor_id: int
    appointment_start: datetime
    appointment_end: datetime


class AppointmentCreate(AppointmentBase):
    """Appointment creation schema."""


class AppointmentResponse(AppointmentBase):
    """Appointment response schema."""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AppointmentWithDetails(AppointmentResponse):
    """Appointment response with patient and doctor details."""

    patient: PatientResponse
    doctor: DoctorResponse


# Update forward references
PatientWithAppointments.model_rebuild()
DoctorWithAppointments.model_rebuild()
