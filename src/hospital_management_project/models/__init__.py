"""Models package."""

from hospital_management_project.models.patient import Patient
from hospital_management_project.models.doctor import Doctor
from hospital_management_project.models.appointment import Appointment

__all__ = ["Patient", "Doctor", "Appointment"]
