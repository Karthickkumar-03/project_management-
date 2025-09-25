from sqlalchemy import Column, Integer, String,Text,DateTime,ForeignKey
from configurations.database import Base
from sqlalchemy.orm import relationship   
from models.base_mixin import AuditMixin
#```````````````````````````````task status````````````````````````````````````````````` 
class TaskStatus(Base,AuditMixin):
    __tablename__ = "task_status"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    tasks = relationship("Task")
#```````````````````````````````task priority`````````````````````````````````````````````
class TaskPriority(Base,AuditMixin):
    __tablename__ = "task_priority"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    tasks = relationship("Task")
#```````````````````````````````task`````````````````````````````````````````````
class Task(Base, AuditMixin):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    start_date = Column(DateTime)
    due_date = Column(DateTime)
    
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    status_id = Column(Integer, ForeignKey("task_status.id"), nullable=False)
    priority_id = Column(Integer, ForeignKey("task_priority.id"), nullable=False)
    # Relationships
    project = relationship("Project")
    assignee = relationship("User", foreign_keys=[assigned_to])
    status = relationship("TaskStatus")
    priority = relationship("TaskPriority")

    
    
