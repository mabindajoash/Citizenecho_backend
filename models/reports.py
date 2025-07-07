from sqlalchemy import Column, String, Integer
from models.base_model import Base, BaseModel

class Report(Base, BaseModel):
    __tablename__ = 'reports'
    title = Column(String(100) , nullable=False)
    status = Column(String(100), default="pending")
    description = Column(String(100), nullable=False)