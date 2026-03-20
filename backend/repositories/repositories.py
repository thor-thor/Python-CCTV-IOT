from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from models.models import Train, Camera, Video, AIDetection, Alert, User, VideoStatus, AlertType
from schemas.schemas import (
    TrainCreate, CameraCreate, VideoCreate, 
    AIDetectionCreate, AlertCreate, UserCreate
)
from core.auth import get_password_hash
from core.logging import logger


# ============== User Repository ==============
class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def create(self, user_data: UserCreate) -> User:
        hashed_password = get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            role=user_data.role
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        logger.info(f"Created user: {user.username}")
        return user
    
    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False


# ============== Train Repository ==============
class TrainRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, train_id: int) -> Optional[Train]:
        return self.db.query(Train).filter(Train.id == train_id).first()
    
    def get_by_number(self, train_number: str) -> Optional[Train]:
        return self.db.query(Train).filter(Train.train_number == train_number).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Train]:
        return self.db.query(Train).offset(skip).limit(limit).all()
    
    def create(self, train_data: TrainCreate) -> Train:
        train = Train(**train_data.model_dump())
        self.db.add(train)
        self.db.commit()
        self.db.refresh(train)
        logger.info(f"Created train: {train.train_number}")
        return train
    
    def count(self) -> int:
        return self.db.query(Train).count()


# ============== Camera Repository ==============
class CameraRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, camera_id: int) -> Optional[Camera]:
        return self.db.query(Camera).filter(Camera.id == camera_id).first()
    
    def get_by_train(self, train_id: int) -> List[Camera]:
        return self.db.query(Camera).filter(Camera.train_id == train_id).all()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Camera]:
        return self.db.query(Camera).offset(skip).limit(limit).all()
    
    def create(self, camera_data: CameraCreate) -> Camera:
        camera = Camera(**camera_data.model_dump())
        self.db.add(camera)
        self.db.commit()
        self.db.refresh(camera)
        logger.info(f"Created camera: {camera.camera_id}")
        return camera


# ============== Video Repository ==============
class VideoRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, video_id: int) -> Optional[Video]:
        return self.db.query(Video).filter(Video.id == video_id).first()
    
    def get_all(
        self,
        skip: int = 0,
        limit: int = 10,
        train_number: Optional[str] = None,
        camera_id: Optional[int] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        status: Optional[VideoStatus] = None
    ) -> tuple[List[Video], int]:
        query = self.db.query(Video)
        
        # Join with Train for train_number filtering
        if train_number:
            query = query.join(Train).filter(Train.train_number == train_number)
        
        if camera_id:
            query = query.filter(Video.camera_id == camera_id)
        
        if from_date:
            query = query.filter(Video.stored_timestamp >= from_date)
        
        if to_date:
            query = query.filter(Video.stored_timestamp <= to_date)
        
        if status:
            query = query.filter(Video.status == status)
        
        # Get total count
        total = query.count()
        
        # Apply pagination and ordering
        videos = query.order_by(Video.stored_timestamp.desc()).offset(skip).limit(limit).all()
        
        return videos, total
    
    def get_by_train_today(self, train_id: int) -> int:
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        return self.db.query(Video).filter(
            and_(
                Video.train_id == train_id,
                Video.stored_timestamp >= today_start
            )
        ).count()
    
    def get_today_count(self) -> int:
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        return self.db.query(Video).filter(Video.stored_timestamp >= today_start).count()
    
    def get_total_storage(self) -> float:
        """Get total storage in GB"""
        result = self.db.query(func.sum(Video.file_size)).scalar()
        if result:
            return result / (1024 * 1024 * 1024)  # Convert bytes to GB
        return 0.0
    
    def create(self, video_data: VideoCreate) -> Video:
        video = Video(**video_data.model_dump())
        self.db.add(video)
        self.db.commit()
        self.db.refresh(video)
        logger.info(f"Created video: {video.id}")
        return video


# ============== AI Detection Repository ==============
class AIDetectionRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_video(self, video_id: int) -> Optional[AIDetection]:
        return self.db.query(AIDetection).filter(AIDetection.video_id == video_id).first()
    
    def create(self, detection_data: AIDetectionCreate) -> AIDetection:
        detection = AIDetection(**detection_data.model_dump())
        self.db.add(detection)
        self.db.commit()
        self.db.refresh(detection)
        logger.info(f"Created AI detection: {detection.id}")
        return detection


# ============== Alert Repository ==============
class AlertRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(
        self,
        skip: int = 0,
        limit: int = 10,
        alert_type: Optional[AlertType] = None,
        is_resolved: Optional[int] = None
    ) -> tuple[List[Alert], int]:
        query = self.db.query(Alert)
        
        if alert_type:
            query = query.filter(Alert.alert_type == alert_type)
        
        if is_resolved is not None:
            query = query.filter(Alert.is_resolved == is_resolved)
        
        total = query.count()
        alerts = query.order_by(Alert.created_at.desc()).offset(skip).limit(limit).all()
        
        return alerts, total
    
    def get_today_count(self) -> int:
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        return self.db.query(Alert).filter(Alert.created_at >= today_start).count()
    
    def create(self, alert_data: AlertCreate) -> Alert:
        alert = Alert(**alert_data.model_dump())
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        logger.info(f"Created alert: {alert.id}")
        return alert
    
    def resolve(self, alert_id: int) -> Optional[Alert]:
        alert = self.db.query(Alert).filter(Alert.id == alert_id).first()
        if alert:
            alert.is_resolved = 1
            alert.resolved_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(alert)
        return alert


# ============== Dashboard Repository ==============
class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_summary(self) -> Dict[str, Any]:
        video_repo = VideoRepository(self.db)
        train_repo = TrainRepository(self.db)
        alert_repo = AlertRepository(self.db)
        
        return {
            "total_videos_today": video_repo.get_today_count(),
            "total_trains_monitored": train_repo.count(),
            "alerts_generated": alert_repo.get_today_count(),
            "storage_usage_gb": round(video_repo.get_total_storage(), 2)
        }
