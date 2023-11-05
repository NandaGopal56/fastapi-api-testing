from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from database.base import Base


# class GenderEnum(enum.Enum):
#     MALE = 'Male'
#     FEMALE = 'Female'
#     OTHER = 'Other'


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)

