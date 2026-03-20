from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from core.database import get_db
from schemas.schemas import (
    VideoListResponse, VideoDetailResponse, VideoCreate, VideoResponse,
    DashboardSummary
)
from services.services import VideoService, DashboardService
from core.auth import get_current_user
from models.models import User, VideoStatus
from core.logging import logger

router = APIRouter(prefix="/api", tags=["Videos"])


@router.get("/videos", response_model=VideoListResponse)
def get_videos(
    train_number: Optional[str] = Query(None, description="Filter by train number"),
    camera_id: Optional[int] = Query(None, description="Filter by camera ID"),
    from_date: Optional[datetime] = Query(None, description="Filter from date (YYYY-MM-DD)"),
    to_date: Optional[datetime] = Query(None, description="Filter to date (YYYY-MM-DD)"),
    status: Optional[VideoStatus] = Query(None, description="Filter by video status"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of videos with filtering and pagination"""
    logger.info(
        f"Fetching videos - page: {page}, page_size: {page_size}, "
        f"train_number: {train_number}, camera_id: {camera_id}"
    )
    
    service = VideoService(db)
    return service.get_videos(
        train_number=train_number,
        camera_id=camera_id,
        from_date=from_date,
        to_date=to_date,
        status=status,
        page=page,
        page_size=page_size
    )


@router.get("/videos/{video_id}", response_model=VideoDetailResponse)
def get_video(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get detailed information for a specific video"""
    logger.info(f"Fetching video details for ID: {video_id}")
    
    service = VideoService(db)
    return service.get_video(video_id)


@router.post("/videos", response_model=VideoResponse, status_code=status.HTTP_201_CREATED)
def create_video(
    video_data: VideoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new video record"""
    logger.info(f"Creating video for train: {video_data.train_id}")
    
    service = VideoService(db)
    return service.create_video(video_data)


@router.get("/dashboard/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get dashboard summary with key operational metrics"""
    logger.info("Fetching dashboard summary")
    
    service = DashboardService(db)
    return service.get_summary()
