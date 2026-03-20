from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from schemas.schemas import TrainResponse, TrainCreate, CameraResponse, CameraCreate
from services.services import TrainService, CameraService
from core.auth import get_current_user
from models.models import User
from core.logging import logger

router = APIRouter(prefix="/api", tags=["Trains"])


@router.get("/trains", response_model=List[TrainResponse])
def get_trains(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of all trains"""
    logger.info(f"Fetching trains - skip: {skip}, limit: {limit}")
    
    service = TrainService(db)
    return service.get_trains(skip=skip, limit=limit)


@router.get("/trains/{train_id}", response_model=TrainResponse)
def get_train(
    train_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get train by ID"""
    logger.info(f"Fetching train ID: {train_id}")
    
    service = TrainService(db)
    return service.get_train(train_id)


@router.post("/trains", response_model=TrainResponse, status_code=status.HTTP_201_CREATED)
def create_train(
    train_data: TrainCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new train"""
    logger.info(f"Creating train: {train_data.train_number}")
    
    service = TrainService(db)
    return service.create_train(train_data)


@router.get("/trains/{train_id}/cameras", response_model=List[CameraResponse])
def get_train_cameras(
    train_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get cameras for a specific train"""
    logger.info(f"Fetching cameras for train ID: {train_id}")
    
    service = CameraService(db)
    return service.get_cameras_by_train(train_id)


@router.post("/cameras", response_model=CameraResponse, status_code=status.HTTP_201_CREATED)
def create_camera(
    camera_data: CameraCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new camera"""
    logger.info(f"Creating camera: {camera_data.camera_id}")
    
    service = CameraService(db)
    return service.create_camera(camera_data)
