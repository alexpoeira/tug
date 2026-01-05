from collections import defaultdict
from sqlalchemy.orm import Session
from app.models.position_report import PositionReport
from app.models.vessel import Vessel
import math

TIME_THRESHOLD_SEC = 120
DISTANCE_THRESHOLD_M = 200 # meters
MIN_REPORTS = 3 

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
    """
    Calculate the great-circle distance between two points
    on the Earth (specified in decimal degrees), returns meters.
    """
    R = 6371000  # radius of Earth in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def infer_tug_jobs(db: Session):
    reports = load_reports(db)
    grouped = group_by_entity(reports)
    vessels_metadata = {int(v.mmsi): v.name for v in db.query(Vessel).all()}
    print(vessels_metadata)
    vessels = {k: v for k, v in grouped.items() if k[0] != "tug"}  # all non-tug vessels
    tugs = {k: v for k, v in grouped.items() if k[0] == "tug"}     # tugs

    inferred_jobs = []

    for (_, vessel_id), vessel_reports in vessels.items():
        for (_, tug_id), tug_reports in tugs.items():
            close_timestamps = []

            for vr in vessel_reports:
                for tr in tug_reports:
                    time_diff = abs((vr.timestamp - tr.timestamp).total_seconds())
                    if time_diff <= TIME_THRESHOLD_SEC:
                        d = haversine_m(vr.latitude, vr.longitude, tr.latitude, tr.longitude)
                        if d <= DISTANCE_THRESHOLD_M:
                            close_timestamps.append(vr.timestamp)

            if len(close_timestamps) >= MIN_REPORTS:
                inferred_jobs.append({
                    "vessel_mmsi": vessel_id,
                    "vessel_name": vessels_metadata.get(int(vessel_id)),
                    "tug_mmsi": tug_id,
                    "tug_name": vessels_metadata.get(int(tug_id)),
                    "start_time": min(close_timestamps),
                    "end_time": max(close_timestamps),
                })

    return inferred_jobs