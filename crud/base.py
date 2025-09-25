
from typing import Type, TypeVar, Generic, List, Optional, Any
from sqlalchemy.orm import Session
from pydantic import BaseModel
from configurations.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], name_field: str = "name"):
        self.model = model
        self.name_field = name_field
        self.pk_column = list(self.model.__table__.primary_key.columns)[0]
    # Get by primary key
    def get(self, db: Session, id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.pk_column == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).order_by(self.pk_column.desc()).offset(skip).limit(limit).all()
                        
    def create(self, db: Session, obj_in: CreateSchemaType, created_by: Optional[int] = None) -> ModelType:
        obj_data = obj_in.dict(exclude_unset=True)

        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        obj_data = obj_in.dict(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int) -> Optional[ModelType]:
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    # ---------------- New helper for uniqueness check ----------------
    def get_by_field(self, db: Session, field: str, value: Any) -> Optional[ModelType]:
        """Check if a value exists in a specific column"""
        return db.query(self.model).filter(getattr(self.model, field) == value).first()
