"""
Compatibility stub.

All ORM models MUST inherit from app.db.base.Base.
This file is kept only to avoid legacy import crashes.
"""

from app.db.base import Base  # re-export for legacy imports

__all__ = ["Base"]
