from sqlalchemy import Column, String
from werkzeug.security import generate_password_hash, check_password_hash
from models.base_model import Base, BaseModel

class User(Base, BaseModel):
    __tablename__ = 'users'

    email = Column(String(100), unique=True, nullable=False)
    _password = Column('password', String(128), nullable=False)  # Store hashed password
    name = Column(String(100), nullable=False)
    role = Column(String(50), default='whistleblower')

    @property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, plain_text_password):
        self._password = generate_password_hash(plain_text_password)

    def check_password(self, plain_text_password):
        return check_password_hash(self._password, plain_text_password)
