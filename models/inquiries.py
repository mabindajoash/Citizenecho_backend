from sqlalchemy import Column, String, Integer
from models.base_model import Base, BaseModel

class Inquiry(Base, BaseModel):
    __tablename__ = 'inquiries'
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    message = Column(String(100), nullable=False)
    status = Column(Integer, default=pending)