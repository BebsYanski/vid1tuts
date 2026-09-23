"""Helper functions for blog operations."""

from typing import Any
from sqlmodel import Session


def create_and_refresh(session: Session, obj: Any) -> Any:
    """Add an object to the session, commit, and refresh it."""

    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj
