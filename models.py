from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, index=True)
    amount = Column(Float)
    source = Column(String)  # e.g., room rent, mess fees
    status = Column(String)  # paid, pending, overdue
    date = Column(Date)

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, index=True)
    category = Column(String)  # operational, mess, miscellaneous
    amount = Column(Float)
    date = Column(Date)

class Occupancy(Base):
    __tablename__ = 'occupancies'
    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, index=True)
    total_beds = Column(Integer)
    occupied_beds = Column(Integer)
    date = Column(Date)

class Complaint(Base):
    __tablename__ = 'complaints'
    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, index=True)
    category = Column(String)  # facility, food, behavior
    status = Column(String)  # resolved, pending
    created_at = Column(Date)
    resolved_at = Column(Date, nullable=True)
