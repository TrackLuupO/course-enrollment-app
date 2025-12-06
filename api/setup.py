#!/usr/bin/env python3
"""
Simple database setup script
"""
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./enrollment.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define models directly
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    enrollments = relationship("Enrollment", back_populates="student")

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    credit_units = Column(Integer, nullable=False)
    description = Column(String)
    enrollments = relationship("Enrollment", back_populates="course")

class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    
    __table_args__ = (UniqueConstraint('student_id', 'course_id', name='unique_enrollment'),)
    
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

def setup_database():
    print("🚀 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created")
    
    db = SessionLocal()
    try:
        # Clear existing data
        print("🗑️  Clearing existing data...")
        db.query(Enrollment).delete()
        db.query(Student).delete()
        db.query(Course).delete()
        db.commit()
        
        # Create sample students
        students = [
            Student(name="John Student", email="john@student.com"),
            Student(name="Phebe Student", email="phebe@student.com"),
            Student(name="Zoe Smith", email="zoe.smith@student.com"),
            Student(name="Emily Johnson", email="emily.johnson@student.com")
        ]
        
        for student in students:
            db.add(student)
        db.commit()
        print(f"✅ Created {len(students)} students")
        
        # Create sample courses
        courses = [
            Course(
                title="Introduction to Computer Science",
                code="CS101",
                credit_units=3,
                description="Fundamental concepts of computer science, algorithms, and programming principles."
            ),
            Course(
                title="Web Development Fundamentals",
                code="WD201",
                credit_units=4,
                description="Comprehensive course covering HTML, CSS, JavaScript and modern web development practices."
            ),
            Course(
                title="Data Science Essentials",
                code="DS301",
                credit_units=4,
                description="Introduction to data analysis, visualization, and machine learning concepts."
            ),
            Course(
                title="UI/UX Design Principles",
                code="UX401",
                credit_units=3,
                description="User interface and experience design methodologies and best practices."
            ),
            Course(
                title="Digital Marketing Strategies",
                code="DM501",
                credit_units=3,
                description="Modern digital marketing techniques including SEO, social media, and content marketing."
            ),
            Course(
                title="Mobile App Development",
                code="MA601",
                credit_units=4,
                description="Cross-platform mobile application development using modern frameworks and tools."
            )
        ]
        
        for course in courses:
            db.add(course)
        db.commit()
        print(f"✅ Created {len(courses)} courses")
        
        # Create sample enrollments
        enrollments = [
            Enrollment(student_id=1, course_id=1),
            Enrollment(student_id=1, course_id=2),
            Enrollment(student_id=2, course_id=1),
            Enrollment(student_id=2, course_id=3),
            Enrollment(student_id=3, course_id=4),
            Enrollment(student_id=4, course_id=5),
        ]
        
        for enrollment in enrollments:
            db.add(enrollment)
        db.commit()
        print(f"✅ Created {len(enrollments)} enrollments")
        
        print("\n🎉 Database setup completed successfully!")
        print(f"📊 Total: {len(students)} students, {len(courses)} courses, {len(enrollments)} enrollments")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    setup_database()
