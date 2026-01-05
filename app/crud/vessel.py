from sqlalchemy.orm import Session
from app.models.vessel import Vessel

def upsert_vessel(
    db: Session,
    mmsi: str,
    imo: int,
    name: str,
    type_: str,
    subtype: str = None,
    callsign: str = None
) -> Vessel:
    vessel = db.query(Vessel).filter(Vessel.mmsi == mmsi).first()

    if vessel:
        # always update fields since IMO is guaranteed
        vessel.imo = imo
        vessel.name = name
        vessel.type = type_
        vessel.subtype = subtype
        vessel.callsign = callsign
    else:
        vessel = Vessel(
            mmsi=mmsi,
            imo=imo,
            name=name,
            type=type_,
            subtype=subtype,
            callsign=callsign
        )
        db.add(vessel)

    db.commit()
    db.refresh(vessel)
    return vessel
