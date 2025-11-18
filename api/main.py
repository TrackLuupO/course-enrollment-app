from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import os
from groq import Groq

from .database import SessionLocal, engine, Base
from .models import Student, Course, Enrollment
from .schemas import StudentCreate, StudentOut, CourseCreate, CourseOut, EnrollCreate, TipsRequest

load_dotenv()
Base.metadata.create_all(bind=engine)  # auto-creates DB on start

app = FastAPI(title="Course Enrollment API")

# CORS for Vue frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/students/", response_model=StudentOut)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.post("/courses/", response_model=CourseOut)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@app.post("/enroll/")
def enroll(enroll: EnrollCreate, db: Session = Depends(get_db)):
    db_enroll = Enrollment(**enroll.model_dump())
    try:
        db.add(db_enroll)
        db.commit()
        return {"message": "Enrolled successfully"}
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Student already enrolled in this course")

@app.get("/students/")
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@app.get("/courses/")
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

@app.get("/students/{student_id}/courses/", response_model=list[CourseOut])
def student_courses(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    # return courses for the student via join to avoid relying on ORM relationships
    return db.query(Course).join(Enrollment).filter(Enrollment.student_id == student_id).all()

@app.get("/courses/{course_id}/students/", response_model=list[StudentOut])
def course_students(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return db.query(Student).join(Enrollment).filter(Enrollment.course_id == course_id).all()

@app.post("/genai/study-tips")
def study_tips(request: TipsRequest):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not set")

    client = Groq(api_key=api_key)
    prompt = f"Generate 3-5 clear, practical study tips for the course '{request.course_title}' worth {request.credit_units} credit units. Focus on daily practice, time allocation per credit unit, and useful tools/apps. Return only the list of tips, no intro."

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=300,
        )
        tips = chat_completion.choices[0].message.content.strip().split("\n")
        tips = [tip.strip("-* .123456789").strip() for tip in tips if tip.strip()]
        return {"tips": tips[:5]}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to generate tips")