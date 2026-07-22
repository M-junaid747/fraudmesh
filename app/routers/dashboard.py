from fastapi import APIRouter
from app.database import get_shared_session
from app.models import Alert

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/alerts")
def get_alerts():
    session = get_shared_session()
    alerts = session.query(Alert).order_by(Alert.created_at.desc()).all()
    session.close()

    return [
        {
            "fingerprint": a.fingerprint,
            "banks_involved": a.banks_involved.split(","),
            "alert_type": a.alert_type,
            "created_at": a.created_at,
        }
        for a in alerts
    ]