from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from configurations.database import Base
from sqlalchemy.orm import relationship
from models.base_mixin import AuditMixin
from datetime import datetime
class Project(Base,AuditMixin):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    status_id = Column(Integer, ForeignKey("project_status.id"), nullable=False)
    status = relationship("ProjectStatus")

    priority_id = Column(Integer, ForeignKey("project_priority.id"), nullable=False)
    priority = relationship("ProjectPriority")
    created_by = Column(Integer,ForeignKey("users.user_id"),nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(String(100))


    creator = relationship("User")
    
#``````````````````````````````Project status``````````````````````````````````````````
class ProjectStatus(Base,AuditMixin):
    __tablename__ = "project_status"

    id = Column(Integer, primary_key=True, index=True)
    status_name= Column(String(50), unique=True, nullable=False)

    projects = relationship("Project")
    
#``````````````````````````````Project priority``````````````````````````````````````````

class ProjectPriority(Base,AuditMixin):
    __tablename__ = "project_priority"

    id = Column(Integer, primary_key=True, index=True)
    priority_name = Column(String(50), unique=True, nullable=False)

    projects = relationship("Project")


