from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ui.app import settings

# SQLAlchemy base class
Base = declarative_base()

# Engine (connects to DB)
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
