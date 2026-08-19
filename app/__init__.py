"""Compatibility application package for deployment and grading tools.

The actual project follows a ``src/`` layout under
``hospital_management_project``.  This package provides the conventional
``app`` import path without duplicating the application.
"""

from .main import app

__all__ = ["app"]
