from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from repositories.repositories import (
    UserRepository, TrainRepository, CameraRepository, 
    VideoRepository, AIDetectionRepository, AlertRepository,
    DashboardRepository
)
from schemas.schemas import (
    UserCreate, UserResponse, Token, LoginRequest,
    TrainCreate, TrainResponse,
    CameraCreate, CameraResponse,
    VideoCreate, VideoResponse, VideoDetailResponse, VideoListResponse,
    AIDetectionCreate, AIDetectionResponse,
    AlertCreate, AlertResponse, AlertListResponse,
    DashboardSummary, PaginationParams
)
from models.models import User, Train, Video, Camera, AIDetection, Alert, VideoStatus, AlertType
from core.auth import verify_password, create_access_token, create_refresh_token
from core.exceptions import NotFoundException, BadRequestException, ConflictException
from core.logging import logger


# ============== Auth Service ==============
class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
    
    def login(self, login_data: LoginRequest) -> Token:
        user = self.user_repo.get_by_username(login_data.username)
        if not user or not verify_password(login_data.password, user.hashed_password):
            logger.warning(f"Failed login attempt for username: {login_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        access_token = create_access_token(
            data={"sub": user.id, "username": user.username, "role": user.role.value}
        )
        refresh_token = create_refresh_token(
            data={"sub": user.id, "username": user.username}
        )
        
        logger.info(f"User logged in: {user.username}")
        return Token(access_token=access_token, refresh_token=refresh_token)
    
    def register(self, user_data: UserCreate) -> UserResponse:
        # Check if email already exists
        if self.user_repo.get_by_email(user_data.email):
            raise ConflictException("Email already registered")
        
        # Check if username already exists
        if self.user_repo.get_by_username(user_data.username):
            raise ConflictException("Username already taken")
        
        user = self.user_repo.create(user_data)
        return UserResponse.model_validate(user)


# ============== User Service ==============
class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
    
    def get_user(self, user_id: int) -> UserResponse:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User", user_id)
        return UserResponse.model_validate(user)
    
    def get_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        users = self.user_repo.get_all(skip, limit)
        return [UserResponse.model_validate(u) for u in users]


# ============== Train Service ==============
class TrainService:
    def __init__(self, db: Session):
        self.db = db
        self.train_repo = TrainRepository(db)
    
    def get_train(self, train_id: int) -> TrainResponse:
        train = self.train_repo.get_by_id(train_id)
        if not train:
            raise NotFoundException("Train", train_id)
        return TrainResponse.model_validate(train)
    
    def get_trains(self, skip: int = 0, limit: int = 100) -> List[TrainResponse]:
        trains = self.train_repo.get_all(skip, limit)
        return [TrainResponse.model_validate(t) for t in trains]
    
    def create_train(self, train_data: TrainCreate) -> TrainResponse:
        # Check if train number already exists
        if self.train_repo.get_by_number(train_data.train_number):
            raise ConflictException(f"Train with number {train_data.train_number} already exists")
        
        train = self.train_repo.create(train_data)
        return TrainResponse.model_validate(train)


# ============== Camera Service ==============
class CameraService:
    def __init__(self, db: Session):
        self.db = db
        self.camera_repo = CameraRepository(db)
    
    def get_camera(self, camera_id: int) -> CameraResponse:
        camera = self.camera_repo.get_by_id(camera_id)
        if not camera:
            raise NotFoundException("Camera", camera_id)
        return CameraResponse.model_validate(camera)
    
    def get_cameras_by_train(self, train_id: int) -> List[CameraResponse]:
        cameras = self.camera_repo.get_by_train(train_id)
        return [CameraResponse.model_validate(c) for c in cameras]

    def create_camera(self, camera_data: CameraCreate) -> CameraResponse:
        camera = self.camera_repo.create(camera_data)
        return CameraResponse.model_validate(camera)


# ============== Video Service ==============
class VideoService:
    def __init__(self, db: Session):
        self.db = db
        self.video_repo = VideoRepository(db)
        self.ai_repo = AIDetectionRepository(db)
    
    def get_videos(
        self,
        train_number: Optional[str] = None,
        camera_id: Optional[int] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        status: Optional[VideoStatus] = None,
        page: int = 1,
        page_size: int = 10
    ) -> VideoListResponse:
        skip = (page - 1) * page_size
        videos, total = self.video_repo.get_all(
            skip=skip,
            limit=page_size,
            train_number=train_number,
            camera_id=camera_id,
            from_date=from_date,
            to_date=to_date,
            status=status
        )
        
        total_pages = (total + page_size - 1) // page_size
        
        return VideoListResponse(
            videos=[VideoResponse.model_validate(v) for v in videos],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    
    def get_video(self, video_id: int) -> VideoDetailResponse:
        video = self.video_repo.get_by_id(video_id)
        if not video:
            raise NotFoundException("Video", video_id)
        
        # Get related data
        ai_detection = self.ai_repo.get_by_video(video_id)
        
        return VideoDetailResponse(
            id=video.id,
            train_id=video.train_id,
            camera_id=video.camera_id,
            video_url=video.video_url,
            stored_timestamp=video.stored_timestamp,
            status=video.status,
            duration=video.duration,
            file_size=video.file_size,
            created_at=video.created_at,
            train=TrainResponse.model_validate(video.train) if video.train else None,
            camera=CameraResponse.model_validate(video.camera) if video.camera else None,
            ai_detection=AIDetectionResponse.model_validate(ai_detection) if ai_detection else None
        )
    
    def create_video(self, video_data: VideoCreate) -> VideoResponse:
        video = self.video_repo.create(video_data)
        return VideoResponse.model_validate(video)


# ============== Alert Service ==============
class AlertService:
    def __init__(self, db: Session):
        self.db = db
        self.alert_repo = AlertRepository(db)
    
    def get_alerts(
        self,
        page: int = 1,
        page_size: int = 10,
        alert_type: Optional[AlertType] = None,
        is_resolved: Optional[int] = None
    ) -> AlertListResponse:
        skip = (page - 1) * page_size
        alerts, total = self.alert_repo.get_all(
            skip=skip,
            limit=page_size,
            alert_type=alert_type,
            is_resolved=is_resolved
        )
        
        return AlertListResponse(
            alerts=[AlertResponse.model_validate(a) for a in alerts],
            total=total,
            page=page,
            page_size=page_size
        )
    
    def create_alert(self, alert_data: AlertCreate) -> AlertResponse:
        alert = self.alert_repo.create(alert_data)
        return AlertResponse.model_validate(alert)
    
    def resolve_alert(self, alert_id: int) -> AlertResponse:
        alert = self.alert_repo.resolve(alert_id)
        if not alert:
            raise NotFoundException("Alert", alert_id)
        return AlertResponse.model_validate(alert)


# ============== Dashboard Service ==============
class DashboardService:
    def __init__(self, db: Session):
        self.db = db
        self.dashboard_repo = DashboardRepository(db)
    
    def get_summary(self) -> DashboardSummary:
        summary = self.dashboard_repo.get_summary()
        return DashboardSummary(**summary)
