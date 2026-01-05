from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.position_report import (
    PositionReportCreate,
    PositionReportRead,
)
from app.db.session import get_db
from app.crud.position_report import (
    get_position_report,
    get_position_reports,
    create_position_report,
)
from app.models.vessel import Vessel
from app.models.position_report import PositionReport
from app.schemas.batch import PositionReportBatch
from fastapi import HTTPException
from dateutil.parser import parse as parse_datetime
from app.crud.vessel import upsert_vessel
from app.schemas.vessel import VesselRead
from app.services.tug_job_inference import infer_tug_jobs

router = APIRouter(prefix="/position-reports", tags=["Position Reports"])

@router.delete("/reset")
def reset_database(db: Session = Depends(get_db)):
    try:
        deleted_reports = db.query(PositionReport).delete()
        deleted_vessels = db.query(Vessel).delete()

        db.commit()
        return {
            "deleted_position_reports": deleted_reports,
            "deleted_vessels": deleted_vessels,
            "status": "Database reset successful"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error resetting database: {str(e)}")

@router.get("/tug-jobs")
def get_inferred_tug_jobs(
    db: Session = Depends(get_db),
    time_threshold_sec: int = Query(120, description="Time threshold in seconds"),
    distance_threshold_m: int = Query(500, description="Distance threshold in meters"),
    min_reports: int = Query(3, description="Minimum number of reports to infer a job")
):
    jobs = infer_tug_jobs(
        db,
        time_threshold_sec=time_threshold_sec,
        distance_threshold_m=distance_threshold_m,
        min_reports=min_reports
    )
    return jobs

@router.get("/vessels", response_model=list[VesselRead])
def get_all_vessels(db: Session = Depends(get_db)):
    vessels = db.query(Vessel).all()
    return vessels

@router.get("/attributes")
def get_unique_attributes(db: Session = Depends(get_db)):
    entity_types = {v.type for v in db.query(Vessel).all()}

    nav_statuses = {r.navigation_status for r in db.query(PositionReport).all()}

    subtypes = {v.subtype for v in db.query(Vessel).all() if v.subtype}

    return {
        "entity_types": sorted(entity_types),
        "navigation_statuses": sorted(nav_statuses),
        "subtypes": sorted(subtypes)
    }

@router.post("/")
def ingest_position_report(payload: PositionReportCreate, db: Session = Depends(get_db)):
    mmsi = str(payload.device.mmsi)

    v = upsert_vessel(
        db=db,
        mmsi=mmsi,
        imo=payload.vessel.imo,
        name=payload.vessel.name,
        type_=payload.vessel.type,
        subtype=payload.vessel.subtype
    )
    print("Vessel upserted:", v.id, v.mmsi, v.name)

    nav = payload.navigation
    return create_position_report(
        db=db,
        entity_type=payload.vessel.type,
        entity_id=mmsi,
        latitude=nav.location.lat,
        longitude=nav.location.long,
        speed=nav.speed,
        course=nav.course,
        navigation_status=nav.status,
        timestamp=nav.time,
    )


@router.get("/", response_model=list[PositionReportRead])
def list_position_reports(db: Session = Depends(get_db)):
    return get_position_reports(db)

@router.get("/{report_id}", response_model=PositionReportRead)
def read_position_report(
    report_id: int,
    db: Session = Depends(get_db),
):
    report = get_position_report(db, report_id)

    if not report:
        raise HTTPException(status_code=404, detail="Position report not found")

    return report

@router.post("/batch")
def ingest_batch(payload: PositionReportBatch, db: Session = Depends(get_db)):
    created = 0

    for record in payload.data:
        mmsi = str(record.device.mmsi)

        v = upsert_vessel(
            db=db,
            mmsi=mmsi,
            imo=record.vessel.imo,
            name=record.vessel.name,
            type_=record.vessel.type,
            callsign=getattr(record.vessel, "callsign", None),
            subtype=getattr(record.vessel, "subtype", None)
        )
        print("Vessel upserted:", v.id, v.mmsi, v.name)

        nav = record.navigation

        create_position_report(
            db=db,
            entity_type=record.vessel.type,
            entity_id=mmsi,
            latitude=nav.location.lat,
            longitude=nav.location.long,
            speed=nav.speed,
            course=nav.course,
            navigation_status=nav.status,
            timestamp=nav.time,
        )
        created += 1

    return {"ingested": created}