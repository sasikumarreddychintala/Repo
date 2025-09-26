from fastapi import FastAPI
from router.reports import router as reports_router
import models
from database import engine
from router import reports
# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hostel Management System")

# Register router
app.include_router(reports.router,prefix="/reports", tags=["Reports"])
