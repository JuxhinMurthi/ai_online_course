from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """ User table. """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)

class Course(Base):
    """ Course table. """

    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_title = Column(String(255), nullable=False)
    course_description = Column(Text, nullable=False)
    ai_summary = Column(Text, nullable=True)
    status = Column(String(50), default="pending")
    created_at = Column(TIMESTAMP, server_default=func.now())
