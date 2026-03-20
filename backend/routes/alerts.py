from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from core.database import get_db
from schemas.schemas import AlertListResponse, AlertResponse, AlertCreate
from services.services import AlertService
from core.auth import get_current_user
from models.models import User, AlertType
from core.logging import logger

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])


@router.get("", response_model=AlertListResponse)
def get_alerts(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    alert_type: Optional[AlertType] = Query(None, description="Filter by alert type"),
    is_resolved: Optional[int] = Query(None, description="Filter by resolution status (0 or 1)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of alerts with filtering and pagination"""
    logger.info(f"Fetching alerts - page: {page}, page_size: {page_size}")
    
    service = AlertService(db)
    return service.get_alerts(
        page=page,
        page_size=page_size,
        alert_type=alert_type,
        is_resolved=is_resolved
    )


@router.post("", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
def create_alert(
    alert_data: AlertCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new alert"""
    logger.info(f"Creating alert for video: {alert_data.video_id}")
    
    service = AlertService(db)
    return service.create_alert(alert_data)


@router.post("/{alert_id}/resolve", response_model=AlertResponse)
def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Resolve an alert"""
    logger.info(f"Resolving alert ID: {alert_id}")
    
    service = AlertService(db)
    return service.resolve_alert(alert_id)
