# routers/reports_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from models import Payment, Expense, Occupancy, Complaint
from schemas import IncomeReport, ExpensesReport, OccupancyReport, ComplaintsReport
from database import SessionLocal
from sqlalchemy import func

router = APIRouter(prefix="/reports", tags=["Reports"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/income", response_model=IncomeReport)
def income_report(hostel_id: int, db: Session = Depends(get_db)):
    payments = db.query(Payment).filter(Payment.hostel_id == hostel_id).all()
    total_income = sum(p.amount for p in payments)
    breakdown = {}
    payment_status = {"paid": 0, "pending": 0, "overdue": 0}
    
    for p in payments:
        breakdown[p.source] = breakdown.get(p.source, 0) + p.amount
        payment_status[p.status] += 1

    return IncomeReport(total_income=total_income, breakdown=breakdown, payment_status=payment_status)

@router.get("/expenses", response_model=ExpensesReport)
def expenses_report(hostel_id: int, db: Session = Depends(get_db)):
    expenses = db.query(Expense).filter(Expense.hostel_id == hostel_id).all()
    total_expenses = sum(e.amount for e in expenses)
    breakdown = {}
    for e in expenses:
        breakdown[e.category] = breakdown.get(e.category, 0) + e.amount

    return ExpensesReport(total_expenses=total_expenses, breakdown=breakdown)

@router.get("/occupancy", response_model=OccupancyReport)
def occupancy_report(hostel_id: int, db: Session = Depends(get_db)):
    records = db.query(Occupancy).filter(Occupancy.hostel_id == hostel_id).order_by(Occupancy.date).all()
    if not records:
        return OccupancyReport(current_rate=0, historical_trends=[])
    
    latest = records[-1]
    current_rate = (latest.occupied_beds / latest.total_beds) * 100 if latest.total_beds else 0
    
    historical_trends = [
        {"date": rec.date, "rate": (rec.occupied_beds / rec.total_beds) * 100 if rec.total_beds else 0}
        for rec in records
    ]
    
    return OccupancyReport(current_rate=current_rate, historical_trends=historical_trends)

@router.get("/complaints", response_model=ComplaintsReport)
def complaints_report(hostel_id: int, db: Session = Depends(get_db)):
    complaints = db.query(Complaint).filter(Complaint.hostel_id == hostel_id).all()
    total = len(complaints)
    resolved = sum(1 for c in complaints if c.status == "resolved")
    pending = sum(1 for c in complaints if c.status == "pending")

    resolution_times = [
        (c.resolved_at - c.created_at).days
        for c in complaints if c.status == "resolved" and c.resolved_at
    ]
    avg_resolution_days = sum(resolution_times) / len(resolution_times) if resolution_times else None

    categorization = {}
    for c in complaints:
        categorization[c.category] = categorization.get(c.category, 0) + 1

    return ComplaintsReport(
        total_complaints=total,
        resolved=resolved,
        pending=pending,
        avg_resolution_days=avg_resolution_days,
        categorization=categorization
    )
