"""
Alerts API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models import Alert, User
from app.schemas.alert import AlertCreate, AlertResponse
from app.api.endpoints.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=AlertResponse)
def create_alert(
    alert: AlertCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new alert"""
    new_alert = Alert(
        user_id=current_user.id,
        **alert.dict()
    )

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    return new_alert


@router.get("/", response_model=List[AlertResponse])
def list_alerts(
    active_only: bool = True,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all alerts for current user"""
    query = db.query(Alert).filter(Alert.user_id == current_user.id)

    if active_only:
        query = query.filter(Alert.is_active == True)

    alerts = query.all()
    return alerts


@router.delete("/{alert_id}")
def delete_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an alert"""
    alert = db.query(Alert).filter(
        Alert.id == alert_id,
        Alert.user_id == current_user.id
    ).first()

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    db.delete(alert)
    db.commit()

    return {"message": "Alert deleted successfully"}
