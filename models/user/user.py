from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from configurations.database import Base
from models.base_mixin import AuditMixin

class Designation(Base, AuditMixin):
    __tablename__ = "designations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

class Department(Base, AuditMixin):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String(50), unique=True, nullable=False)

    designation_id = Column(Integer, ForeignKey("designations.id"),nullable=False)  # <- add this
    designation = relationship("Designation")  # one-way relationship
 # only one-way relationship

class User(Base, AuditMixin):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    role = relationship("Role")

    department_id = Column(Integer, ForeignKey("department.id"))
    department = relationship("Department")  # only one-way relationship
    projects = relationship("Project")


class Role(Base, AuditMixin):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    users = relationship("User")  # optional; can leave it out
