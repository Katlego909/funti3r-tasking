from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, Enrollment, LessonResource, Category, Progress, Chapter
from django.db.models import Count

def home(request):
    return render(request, 'course/home.html')

@login_required
def course_list(request):
    categories = Category.objects.all()
    courses_by_category = {}

    for category in categories:
        courses = Course.objects.filter(category=category)
        courses_by_category[category] = courses

    return render(request, 'course/course_list.html', {'courses_by_category': courses_by_category})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    
    if request.method == 'POST' and not enrolled:  # Process enrollment form submission
        Enrollment.objects.create(student=request.user, course=course)
        return redirect('course_detail', course_id=course.id)
    
    lessons = course.get_lessons()
    lesson_count = lessons.count()  # Count of lessons for the course
    return render(request, 'course/course_detail.html', {'course': course, 'enrolled': enrolled, 'lessons': lessons, 'lesson_count': lesson_count})

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    if request.method == 'POST':  # Process enrollment form submission
        Enrollment.objects.get_or_create(student=request.user, course=course)
        return redirect('course_detail', course_id=course.id)
    
    return render(request, 'course/enroll_course.html', {'course': course})

@login_required
def unenroll_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.filter(student=request.user, course=course).first()
    
    if enrollment:
        enrollment.delete()  # Delete the enrollment record
    return redirect('course_detail', course_id=course.id)

@login_required
def lesson_detail(request, course_id, lesson_id):
    course = get_object_or_404(Course, pk=course_id)
    lesson = get_object_or_404(Lesson, pk=lesson_id, course=course)
    enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()

    # Check if the lesson is completed for the current user
    lesson_completed = Progress.objects.filter(student=request.user, lesson=lesson, completed=True).exists()

    if not enrolled:
        # Redirect to course detail if not enrolled
        return redirect('course_detail', course_id=course.id)

    chapters = lesson.chapters.all()

    resources = lesson.resources.all()

    return render(request, 'course/lesson_detail.html', {'lesson': lesson, 'chapters': chapters, 'resources': resources, 'lesson_completed': lesson_completed})

@login_required
def chapter_detail(request, course_id, lesson_id, chapter_id):
    course = get_object_or_404(Course, pk=course_id)
    lesson = get_object_or_404(Lesson, pk=lesson_id, course=course)
    chapter = get_object_or_404(Chapter, pk=chapter_id, lesson=lesson)
    enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()

    if not enrolled:
        return redirect('course_detail', course_id=course.id)

    resources = chapter.resource.all()

    return render(request, 'course/chapter_detail.html', {'chapter': chapter, 'resources': resources})

@login_required
def lesson_resource(request, course_id, lesson_id, resource_id):
    course = get_object_or_404(Course, pk=course_id)
    lesson = get_object_or_404(Lesson, pk=lesson_id, course=course)
    enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    if not enrolled:
        # Redirect to course detail if not enrolled
        return redirect('course_detail', course_id=course.id)
    resource = get_object_or_404(LessonResource, pk=resource_id, lesson=lesson)
    return render(request, 'course/lesson_resource.html', {'resource': resource})

@login_required
def mark_as_complete(request, lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    course = lesson.course
    student = request.user

    # Check if the progress record already exists
    progress_record, created = Progress.objects.get_or_create(student=student, course=course, lesson=lesson)

    if created or not progress_record.completed:
        progress_record.completed = True
        progress_record.save()

    return redirect('course_detail', course_id=course.id)

@login_required
def learner_progress(request):
    student = request.user

    # Calculate learner progress
    completed_lessons = Progress.objects.filter(student=student, completed=True).values('course').annotate(total=Count('lesson')).values_list('total', flat=True)
    total_lessons = Course.objects.annotate(total_lessons=Count('lessons')).filter(progress__student=student).distinct().values_list('total_lessons', flat=True)

    if total_lessons:
        progress_percentage = sum(completed_lessons) / sum(total_lessons) * 100
    else:
        progress_percentage = 0

    return render(request, 'course/learner_progress.html', {'progress_percentage': progress_percentage})

