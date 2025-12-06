from pydantic import BaseModel
from typing import Optional

class StudentCreate(BaseModel):
    name: str
    email: str

class StudentOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class CourseCreate(BaseModel):
    title: str
    code: str
    credit_units: int
    description: Optional[str] = None

class CourseOut(BaseModel):
    id: int
    title: str
    code: str
    credit_units: int
    description: Optional[str]

    class Config:
        from_attributes = True

class EnrollCreate(BaseModel):
    student_id: int
    course_id: int

class EnrollmentOut(BaseModel):
    id: int
    student_id: int
    course_id: int

    class Config:
        from_attributes = True

class TipsRequest(BaseModel):
    course_title: str
    credit_units: int

class Statistics(BaseModel):
    total_students: int
    total_courses: int
    total_enrollments: int
