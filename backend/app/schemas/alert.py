"""
Alert Pydantic schemas
"""
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class AlertCreate(BaseModel):
    """Alert creation schema"""
    company_id: int
    alert_type: str
    condition_field: Optional[str] = None
    condition_operator: Optional[str] = None
    condition_value: Optional[float] = None
    keywords: Optional[str] = None
    title: str
    message: Optional[str] = None
    notify_email: bool = True
    notify_app: bool = True
    expires_at: Optional[datetime] = None


class AlertResponse(BaseModel):
    """Alert response schema"""
    id: int
    company_id: int
    alert_type: str
    title: str
    is_active: bool
    is_triggered: bool
    triggered_at: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
