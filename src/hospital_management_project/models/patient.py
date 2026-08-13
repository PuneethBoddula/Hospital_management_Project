"""Patient model."""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from hospital_management_project.database import Base


class Patient(Base):
    """Patient database model."""

    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")
