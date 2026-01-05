from fastapi import FastAPI
from app.api import position_reports

app = FastAPI(title="Tug Job Inference API")

app.include_router(position_reports.router)

@app.get("/")
def root():
    return {"status": "running"}
