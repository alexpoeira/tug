from sqlalchemy.orm import Session
from app.models.position_report import PositionReport

def create_position_report(
    db: Session,
    *,
    entity_type: str,
    entity_id: int,
    latitude: float,
    longitude: float,
    speed: float | None,
    course: float | None,
    navigation_status: str | None,
    timestamp
):
    report = PositionReport(
        entity_type=entity_type,
        entity_id=entity_id,
        latitude=latitude,
        longitude=longitude,
        speed=speed,
        course=course,
        navigation_status=navigation_status,
        timestamp=timestamp,
    )

    db.add(report)
    db.commit()
    db.refresh(report)
    return report

def get_position_report(db: Session, report_id: int):
    return (
        db.query(PositionReport)
        .filter(PositionReport.id == report_id)
        .first()
    )

def get_position_reports(db: Session):
    return (
        db.query(PositionReport)
        .order_by(PositionReport.timestamp)
        .all()
    )