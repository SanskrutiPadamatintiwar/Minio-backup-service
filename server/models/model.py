
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from services.dbconnection import Base

class FileUpload(Base):
    __tablename__ = "file_uploads"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    content_type = Column(String(100))
    timestamp = Column(DateTime, default=datetime.now(), index=True)
    file_path = Column(String(500), nullable=False)
    is_synced = Column(Boolean, default=False)
    last_synced = Column(DateTime, nullable=True)
