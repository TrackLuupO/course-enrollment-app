from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from typing import List
from dotenv import load_dotenv
import os
from groq import Groq

# Change from relative imports to direct imports
from database import SessionLocal, engine, Base
from models import Student, Course, Enrollment
from schemas import StudentCreate, StudentOut, CourseCreate, CourseOut, EnrollCreate, TipsRequest

load_dotenv()
Base.metadata.create_all(bind=engine)  # auto-creates DB on start

app = FastAPI(title="Course Enrollment API")

# CORS for Vue frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:8080", 
        "http://localhost:5173", 
        "http://localhost:8000",
        "http://localhost:8082",  # Frontend port
        "http://127.0.0.1:8082",  # Frontend IP
        "http://127.0.0.1:8080",  # Alternative frontend port
        "http://10.210.242.101:8082"  # Your network IP
    ],
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

# Student Endpoints
@app.post("/students/", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_student = db.query(Student).filter(Student.email == student.email).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/", response_model=List[StudentOut])
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@app.get("/students/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Course Endpoints
@app.post("/courses/", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    # Check if course code already exists
    existing_course = db.query(Course).filter(Course.code == course.code).first()
    if existing_course:
        raise HTTPException(status_code=400, detail="Course code already exists")
    
    db_course = Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@app.get("/courses/", response_model=List[CourseOut])
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

@app.get("/courses/{course_id}", response_model=CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.put("/courses/{course_id}", response_model=CourseOut)
def update_course(course_id: int, course: CourseCreate, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check if new course code conflicts with existing course (excluding current)
    if course.code != db_course.code:
        existing_course = db.query(Course).filter(Course.code == course.code).first()
        if existing_course:
            raise HTTPException(status_code=400, detail="Course code already exists")
    
    # Update course fields
    db_course.title = course.title
    db_course.code = course.code
    db_course.credit_units = course.credit_units
    db_course.description = course.description
    
    db.commit()
    db.refresh(db_course)
    return db_course

@app.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    # Check if course exists
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check if any students are enrolled in this course
    enrollments_count = db.query(Enrollment).filter(Enrollment.course_id == course_id).count()
    if enrollments_count > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete course with {enrollments_count} enrolled student(s). Unenroll all students first."
        )
    
    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully"}

# Enrollment Endpoints
@app.post("/enrollments/", status_code=status.HTTP_201_CREATED)
def create_enrollment(enroll: EnrollCreate, db: Session = Depends(get_db)):
    # Check if student exists
    student = db.query(Student).filter(Student.id == enroll.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if course exists
    course = db.query(Course).filter(Course.id == enroll.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check if enrollment already exists
    existing_enrollment = db.query(Enrollment).filter(
        Enrollment.student_id == enroll.student_id,
        Enrollment.course_id == enroll.course_id
    ).first()
    
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="Student already enrolled in this course")
    
    db_enrollment = Enrollment(**enroll.model_dump())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return {"message": "Enrollment created successfully", "id": db_enrollment.id}

@app.get("/enrollments/")
def get_enrollments(db: Session = Depends(get_db)):
    return db.query(Enrollment).all()

@app.get("/enrollments/student/{student_id}")
def get_student_enrollments(student_id: int, db: Session = Depends(get_db)):
    enrollments = db.query(Enrollment).filter(Enrollment.student_id == student_id).all()
    return [
        {
            "enrollment_id": e.id,
            "student_id": e.student_id,
            "course_id": e.course_id,
            "course": db.query(Course).filter(Course.id == e.course_id).first()
        }
        for e in enrollments
    ]

@app.get("/enrollments/course/{course_id}")
def get_course_enrollments(course_id: int, db: Session = Depends(get_db)):
    enrollments = db.query(Enrollment).filter(Enrollment.course_id == course_id).all()
    return [
        {
            "enrollment_id": e.id,
            "student_id": e.student_id,
            "course_id": e.course_id,
            "student": db.query(Student).filter(Student.id == e.student_id).first()
        }
        for e in enrollments
    ]

@app.delete("/enrollments/{enrollment_id}")
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    db.delete(enrollment)
    db.commit()
    return {"message": "Enrollment deleted successfully"}

@app.get("/stats/")
def get_statistics(db: Session = Depends(get_db)):
    total_students = db.query(Student).count()
    total_courses = db.query(Course).count()
    total_enrollments = db.query(Enrollment).count()
    
    return {
        "total_students": total_students,
        "total_courses": total_courses,
        "total_enrollments": total_enrollments
    }

@app.post("/genai/study-tips")
def study_tips(request: TipsRequest):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not set")

    client = Groq(api_key=api_key)
    
    # Use provided course info or defaults for general tips
    course_title = request.course_title or "General Studies"
    credit_units = request.credit_units or 3
    
    prompt = f"Generate 3-5 clear, practical study tips for the course '{course_title}' worth {credit_units} credit units. Focus on daily practice, time allocation per credit unit, and useful tools/apps. Return only the list of tips, no intro."

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
             # Fast and reliable model
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=100,
        )
        tips = chat_completion.choices[0].message.content.strip().split("\n")
        tips = [tip.strip("-* .123456789").strip() for tip in tips if tip.strip()]
        return {"tips": tips[:5]}
    except Exception as e:
        print(f"Groq API error: {e}")  # For debugging
        # Return default tips if API fails
        default_tips = [
            f"For {course_title} ({credit_units} credits), allocate {credit_units * 2} hours per week for study.",
            "Break your study sessions into 25-minute focused blocks with 5-minute breaks (Pomodoro Technique).",
            "Teach the material to someone else - explaining concepts reinforces your understanding.",
            f"Create flashcards for key concepts in {course_title} and review them daily.",
            f"Form a study group for {course_title} to discuss difficult topics.",
            "Use spaced repetition - review material at increasing intervals for better retention."
        ]
        # Shuffle and return 4 tips
        import random
        return {"tips": random.sample(default_tips, 4)}

@app.get("/")
def root():
    return {"message": "Course Enrollment System API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
