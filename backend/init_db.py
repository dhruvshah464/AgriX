import sys
from pathlib import Path

# Provide import resolution for backend modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.app.db.session import engine
# Import base to ensure all models are registered with SQLAlchemy metadata
from backend.app.db.base import *
from backend.app.models.base import Base

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
