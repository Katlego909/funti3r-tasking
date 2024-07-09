from ninja import Schema
from typing import List, Optional
from pydantic import Field
from datetime import datetime

class CategorySchema(Schema):
    id: int
    name: str
    description: Optional[str] = None

class CourseSchema(Schema):
    id: int
    title: str
    category_id: int
    instructor_id: int
    description: str
    price: float
    image: Optional[str] = None
    created_at: datetime
    experience_level: str
    duration: str

class LessonSchema(Schema):
    id: int
    title: str
    course_id: int
    order: int
    content: str
    image: Optional[str] = None

class ChapterSchema(Schema):
    id: int
    lesson_id: int
    title: str
    order: int
    content: str

class ResourceSchema(Schema):
    id: int
    chapter_id: int
    title: str
    file: str

class LessonResourceSchema(Schema):
    id: int
    lesson_id: int
    title: str
    resource_file: str

class EnrollmentSchema(Schema):
    id: int
    student_id: int
    course_id: int
    enrolled_at: datetime

class ProgressSchema(Schema):
    id: int
    student_id: int
    course_id: int
    lesson_id: int
    completed: bool
