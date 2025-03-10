from datetime import datetime
from pydantic import BaseModel


class UserCreate(BaseModel):
    """ Create new user schema. """

    name: str
    email: str

class User(BaseModel):
    """ User schema. """

    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

class CourseCreate(BaseModel):
    """ Create new course schema. """

    user_id: int
    course_title: str
    course_description: str

class Course(BaseModel):
    """ Course schema. """

    id: int
    user_id: int
    course_title: str
    course_description: str
    ai_summary: str | None = None
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
