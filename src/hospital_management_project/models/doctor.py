"""Doctor model."""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from hospital_management_project.database import Base


class Doctor(Base):
    """Doctor database model."""

    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    specialization = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    appointments = relationship("Appointment", back_populates="doctor", cascade="all, delete-orphan")
