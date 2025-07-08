from sqlalchemy import Column, String, ForeignKey, Integer
from models.base_model import Base, BaseModel

class User(Base, BaseModel):
    __tablename__ = 'users'
    email = Column(String, unique=True)
    password = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)