from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from configurations.database import Base
from models.base_mixin import AuditMixin

class Bug(Base, AuditMixin):
    __tablename__ = "bugs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    # Foreign keys
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    reporter_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    assignee_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    status_id = Column(Integer, ForeignKey("bug_status.id"), nullable=False)
    priority_id = Column(Integer, ForeignKey("bug_priority.id"), nullable=False)
    environment_id = Column(Integer, ForeignKey("bug_environment.id"), nullable=True)

    # Relationships
    project = relationship("Project")
    reporter = relationship("User", foreign_keys=[reporter_id])
    assignee = relationship("User", foreign_keys=[assignee_id])
    status = relationship("BugStatus")
    priority = relationship("BugPriority")
    environment = relationship("BugEnvironment")


# ---------------- Bug Status ----------------
class BugStatus(Base, AuditMixin):
    __tablename__ = "bug_status"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    bugs = relationship("Bug")


# ---------------- Bug Priority ----------------
class BugPriority(Base, AuditMixin):
    __tablename__ = "bug_priority"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    bugs = relationship("Bug")


# ---------------- Bug Environment ----------------
class BugEnvironment(Base, AuditMixin):
    __tablename__ = "bug_environment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    bugs = relationship("Bug")
