from collections import defaultdict
from sqlalchemy.orm import Session
from app.models.position_report import PositionReport
from app.models.vessel import Vessel
import math

def load_reports(db: Session):
    return (
        db.query(PositionReport)
        .order_by(PositionReport.timestamp)
        .all()
    )

def group_by_entity(reports):
    grouped = defaultdict(list)

    for r in reports:
        key = (r.entity_type, r.entity_id)
        grouped[key].append(r)

    return grouped

def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def infer_tug_jobs(
    db: Session,
    time_threshold_sec: int = 120,
    distance_threshold_m: int = 500,
    min_reports: int = 3,
):
    reports = load_reports(db)
    grouped = group_by_entity(reports)
    vessels_metadata = {int(v.mmsi): v.name for v in db.query(Vessel).all()}

    vessels = {k: v for k, v in grouped.items() if k[0] != "tug"}
    tugs = {k: v for k, v in grouped.items() if k[0] == "tug"}

    inferred_jobs = []

    for (_, vessel_id), vessel_reports in vessels.items():
        for (_, tug_id), tug_reports in tugs.items():
            close_timestamps = []

            for vr in vessel_reports:
                for tr in tug_reports:
                    time_diff = abs((vr.timestamp - tr.timestamp).total_seconds())
                    if time_diff <= time_threshold_sec:
                        d = haversine_m(vr.latitude, vr.longitude, tr.latitude, tr.longitude)
                        if d <= distance_threshold_m:
                            close_timestamps.append(vr.timestamp)

            if len(close_timestamps) >= min_reports:
                inferred_jobs.append({
                    "vessel_mmsi": vessel_id,
                    "vessel_name": vessels_metadata.get(int(vessel_id)),
                    "tug_mmsi": tug_id,
                    "tug_name": vessels_metadata.get(int(tug_id)),
                    "start_time": min(close_timestamps),
                    "end_time": max(close_timestamps),
                })

    return inferred_jobs