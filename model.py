from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# Database connection (Update credentials as needed)
DATABASE_URL = "postgresql://postgres:amogh123@localhost/contacts"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
Base.metadata.clear()

# Contact Model
class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=False, nullable=True)
    phone = Column(String, unique=False, nullable=True)
    
    linkprecedence_phone = Column(Boolean, default=False, nullable=False)
    linkprecedence_email = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=func.now())
    modified_at = Column(DateTime, default=func.now(), onupdate=func.now())

    
    
# Create tables
Base.metadata.create_all(engine)
