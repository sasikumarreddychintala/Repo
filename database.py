from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
 
# Change this to your PostgreSQL connection string
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/PORTS"
 
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
Base = declarative_base()
get_db = SessionLocal
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()