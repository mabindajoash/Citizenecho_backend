from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from models.base_model import Base, BaseModel

class ReportAssignment(Base, BaseModel):
    __tablename__ = 'report_assignments'

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    report_id = Column(String(60), ForeignKey('reports.id'), nullable=False)
    role = Column(String(100), default='whistleblower')
    
    user = relationship("User", backref=backref("report_assignments", cascade="all, delete-orphan"))
    report = relationship("Report", backref=backref("report_assignments", cascade="all, delete-orphan"))
