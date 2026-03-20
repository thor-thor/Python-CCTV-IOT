from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum, Float, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base
import enum


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"


class VideoStatus(str, enum.Enum):
    AVAILABLE = "available"
    PROCESSING = "processing"
    FAILED = "failed"


class AIStatus(str, enum.Enum):
    PENDING = "pending"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"


class AlertType(str, enum.Enum):
    MOTION_DETECTED = "motion_detected"
    OBJECT_DETECTED = "object_detected"
    ANOMALY = "anomaly"
    ERROR = "error"


class Train(Base):
    """Train model"""
    __tablename__ = "trains"
    
    id = Column(Integer, primary_key=True, index=True)
    train_number = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    cameras = relationship("Camera", back_populates="train")
    videos = relationship("Video", back_populates="train")
    
    __table_args__ = (
        Index('idx_train_number', 'train_number'),
    )


class Camera(Base):
    """Camera model"""
    __tablename__ = "cameras"
    
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer, ForeignKey("trains.id"), nullable=False)
    camera_id = Column(String(50), nullable=False, index=True)
    location = Column(String(255), nullable=True)  # e.g., "Engine", "Coach 1", "Corridor"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    train = relationship("Train", back_populates="cameras")
    videos = relationship("Video", back_populates="camera")
    
    __table_args__ = (
        Index('idx_camera_train', 'train_id', 'camera_id'),
    )


class Video(Base):
    """Video model"""
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer, ForeignKey("trains.id"), nullable=False)
    camera_id = Column(Integer, ForeignKey("cameras.id"), nullable=False)
    video_url = Column(Text, nullable=False)  # S3 URL
    stored_timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    status = Column(Enum(VideoStatus), default=VideoStatus.PROCESSING, nullable=False)
    duration = Column(Float, nullable=True)  # Duration in seconds
    file_size = Column(Integer, nullable=True)  # Size in bytes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    train = relationship("Train", back_populates="videos")
    camera = relationship("Camera", back_populates="videos")
    ai_detections = relationship("AIDetection", back_populates="video")
    alerts = relationship("Alert", back_populates="video")
    
    __table_args__ = (
        Index('idx_video_train_timestamp', 'train_id', 'stored_timestamp'),
        Index('idx_video_camera_timestamp', 'camera_id', 'stored_timestamp'),
        Index('idx_video_status', 'status'),
    )


class AIDetection(Base):
    """AI Detection results model"""
    __tablename__ = "ai_detections"
    
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    ai_status = Column(Enum(AIStatus), default=AIStatus.PENDING, nullable=False)
    detected_objects = Column(Text, nullable=True)  # JSON string of detected objects
    confidence_score = Column(Float, nullable=True)
    anomalies = Column(Text, nullable=True)  # JSON string of anomalies
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    video = relationship("Video", back_populates="ai_detections")
    
    __table_args__ = (
        Index('idx_ai_detection_video', 'video_id'),
    )


class Alert(Base):
    """Alert model"""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    alert_type = Column(Enum(AlertType), nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(String(20), default="medium")  # low, medium, high
    is_resolved = Column(Integer, default=0)  # 0 = false, 1 = true
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    video = relationship("Video", back_populates="alerts")
    
    __table_args__ = (
        Index('idx_alert_video', 'video_id'),
        Index('idx_alert_type', 'alert_type'),
        Index('idx_alert_created', 'created_at'),
    )


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_user_email', 'email'),
        Index('idx_user_role', 'role'),
    )
