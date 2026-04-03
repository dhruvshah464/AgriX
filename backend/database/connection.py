"""Backward-compatible DB connection export for earlier scaffold."""

from backend.app.db.session import engine

__all__ = ["engine"]
