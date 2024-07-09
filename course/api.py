from ninja import NinjaAPI
from .models import Category, Course, Lesson, Chapter, Resource, LessonResource, Enrollment, Progress
from .schemas import CategorySchema, CourseSchema, LessonSchema, ChapterSchema, ResourceSchema, LessonResourceSchema, EnrollmentSchema, ProgressSchema
from typing import List
from django.shortcuts import get_object_or_404

api = NinjaAPI()

@api.get("/categories", response=List[CategorySchema])
def list_categories(request):
    return Category.objects.all()

@api.get("/categories/{category_id}", response=CategorySchema)
def get_category(request, category_id: int):
    category = get_object_or_404(Category, id=category_id)
    return category

@api.get("/courses", response=List[CourseSchema])
def list_courses(request):
    return Course.objects.all()

@api.get("/courses/{course_id}", response=CourseSchema)
def get_course(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    return course

@api.get("/lessons", response=List[LessonSchema])
def list_lessons(request):
    return Lesson.objects.all()

@api.get("/lessons/{lesson_id}", response=LessonSchema)
def get_lesson(request, lesson_id: int):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return lesson

@api.get("/chapters", response=List[ChapterSchema])
def list_chapters(request):
    return Chapter.objects.all()

@api.get("/chapters/{chapter_id}", response=ChapterSchema)
def get_chapter(request, chapter_id: int):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    return chapter

@api.get("/resources", response=List[ResourceSchema])
def list_resources(request):
    return Resource.objects.all()

@api.get("/resources/{resource_id}", response=ResourceSchema)
def get_resource(request, resource_id: int):
    resource = get_object_or_404(Resource, id=resource_id)
    return resource

@api.get("/lesson-resources", response=List[LessonResourceSchema])
def list_lesson_resources(request):
    return LessonResource.objects.all()

@api.get("/lesson-resources/{lesson_resource_id}", response=LessonResourceSchema)
def get_lesson_resource(request, lesson_resource_id: int):
    lesson_resource = get_object_or_404(LessonResource, id=lesson_resource_id)
    return lesson_resource

@api.get("/enrollments", response=List[EnrollmentSchema])
def list_enrollments(request):
    return Enrollment.objects.all()

@api.get("/enrollments/{enrollment_id}", response=EnrollmentSchema)
def get_enrollment(request, enrollment_id: int):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    return enrollment

@api.get("/progress", response=List[ProgressSchema])
def list_progress(request):
    return Progress.objects.all()

@api.get("/progress/{progress_id}", response=ProgressSchema)
def get_progress(request, progress_id: int):
    progress = get_object_or_404(Progress, id=progress_id)
    return progress
