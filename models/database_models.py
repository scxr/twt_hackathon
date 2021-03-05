from db.base import Base
from sqlalchemy import Boolean, Column, Integer, String, Float
from sqlalchemy.types import DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from random import randint

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String,index=True, unique=True)
    hashed_pword = Column(String)