from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from models.models import UserRole, VideoStatus, AIStatus, AlertType


# ============== User Schemas ==============
class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.USER


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[int] = None


class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = None
    role: Optional[UserRole] = None


class LoginRequest(BaseModel):
    username: str
    password: str


# ============== Train Schemas ==============
class TrainBase(BaseModel):
    train_number: str
    name: str


class TrainCreate(TrainBase):
    pass


class TrainResponse(TrainBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============== Camera Schemas ==============
class CameraBase(BaseModel):
    camera_id: str
    location: Optional[str] = None


class CameraCreate(CameraBase):
    train_id: int


class CameraResponse(CameraBase):
    id: int
    train_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============== Video Schemas ==============
class VideoBase(BaseModel):
    video_url: str
    stored_timestamp: datetime
    status: VideoStatus = VideoStatus.PROCESSING
    duration: Optional[float] = None
    file_size: Optional[int] = None


class VideoCreate(VideoBase):
    train_id: int
    camera_id: int


class VideoResponse(BaseModel):
    id: int
    train_id: int
    camera_id: int
    video_url: str
    stored_timestamp: datetime
    status: VideoStatus
    duration: Optional[float] = None
    file_size: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class VideoDetailResponse(VideoResponse):
    train: Optional[TrainResponse] = None
    camera: Optional[CameraResponse] = None
    ai_detection: Optional['AIDetectionResponse'] = None
    
    class Config:
        from_attributes = True


class VideoListResponse(BaseModel):
    videos: List[VideoResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


# ============== AI Detection Schemas ==============
class AIDetectionBase(BaseModel):
    ai_status: AIStatus = AIStatus.PENDING
    detected_objects: Optional[str] = None
    confidence_score: Optional[float] = None
    anomalies: Optional[str] = None


class AIDetectionCreate(AIDetectionBase):
    video_id: int


class AIDetectionResponse(AIDetectionBase):
    id: int
    video_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============== Alert Schemas ==============
class AlertBase(BaseModel):
    alert_type: AlertType
    message: str
    severity: str = "medium"


class AlertCreate(AlertBase):
    video_id: int


class AlertResponse(AlertBase):
    id: int
    video_id: int
    is_resolved: int
    created_at: datetime
    resolved_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AlertListResponse(BaseModel):
    alerts: List[AlertResponse]
    total: int
    page: int
    page_size: int


# ============== Dashboard Schemas ==============
class DashboardSummary(BaseModel):
    total_videos_today: int
    total_trains_monitored: int
    alerts_generated: int
    storage_usage_gb: float


# ============== Pagination Schemas ==============
class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)


# Update forward references
VideoDetailResponse.model_rebuild()
