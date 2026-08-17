"""Allow the application to be imported directly from a source checkout.

The production package lives in ``src/``.  This compatibility package lets
test runners that execute from the repository root import it without first
performing an editable installation.
"""

from pathlib import Path

__path__ = [str(Path(__file__).resolve().parent.parent / "src" / "hospital_management_project")]

from .database import Base, SessionLocal, engine, get_db

__all__ = ["Base", "SessionLocal", "engine", "get_db"]
