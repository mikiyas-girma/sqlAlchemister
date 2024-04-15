from sqlalchemy import (create_engine, String, Integer,
                        Column, func, ForeignKey, or_,
                        Sequence, join)
from sqlalchemy.orm import (declarative_base, sessionmaker, relationship,
                            Mapped, mapped_column, joinedload)

engine = create_engine(
    'postgresql://postgres:Mm1122@localhost:5432/school', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(255))

    students = relationship("Student", secondary="course_enrollments",
                            backref="enrolled_in")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50))

    # courses = relationship("Course", secondary="course_enrollments",
    #                        backref="students")


class CourseEnrollment(Base):
    __tablename__ = "course_enrollments"

    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), primary_key=True)


def get_or_create_student(name, email):
    """Function to get or create a student
    """
    student = session.query(Student).filter_by(name=name, email=email).first()
    if not student:
        student = Student(name=name, email=email)
    return student


math_course = Course(name="Math", description="Advanced Mathematics")
english_course = Course(name="English", description="English Literature")


john = get_or_create_student(name="John", email="john@example.com")

english = session.query(Course).filter(Course.name == "English").one()
english.students.append(john)

session.commit()
