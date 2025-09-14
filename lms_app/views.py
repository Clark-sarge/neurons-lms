
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Course, Module, Content, User
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
@require_POST
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user.role == 'student':
        request.user.enrolled_courses.add(course)
        messages.success(request, f'Enrolled in {course.title}.')
    return redirect('course_list')

@login_required
@require_POST
def unenroll_from_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user.role == 'student':
        request.user.enrolled_courses.remove(course)
        messages.success(request, f'Unenrolled from {course.title}.')
    return redirect('course_list')

def home(request):
    return render(request, 'home.html')

@login_required
def admin_dashboard(request):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('home')

    if request.method == 'POST':
        # Handle course creation
        title = request.POST.get('title')
        code = request.POST.get('code')
        description = request.POST.get('description')
        instructor = request.POST.get('instructor')
        semester = request.POST.get('semester')
        year = request.POST.get('year')
        if all([title, code, instructor, semester, year]):
            if Course.objects.filter(code=code).exists():
                messages.error(request, 'A course with this code already exists.')
            else:
                Course.objects.create(
                    title=title,
                    code=code,
                    description=description or '',
                    instructor=instructor,
                    semester=semester,
                    year=year
                )
                messages.success(request, f'Course {title} created successfully!')
        else:
            messages.error(request, 'All required fields must be filled.')

    courses = Course.objects.all().order_by('title')
    return render(request, 'admin_dashboard.html', {'courses': courses})

@login_required
def course_list(request):
    # Redirect superusers/admins to admin dashboard
    if request.user.is_superuser or request.user.role == 'admin':
        return redirect('admin_dashboard')
    if request.user.role == 'instructor':
        courses = Course.objects.filter(instructor=request.user)
    else:
        courses = request.user.enrolled_courses.all()
    return render(request, 'course_list.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Check permissions
    if request.user.role == 'student' and not course.students.filter(id=request.user.id).exists():
        messages.error(request, 'You are not enrolled in this course.')
        return redirect('course_list')
    
    modules = course.modules.filter(parent=None).order_by('order')
    return render(request, 'course_detail.html', {
        'course': course,
        'modules': modules
    })

@login_required
def user_management(request):
    if request.user.role not in ['admin', 'instructor']:
        messages.error(request, 'Permission denied.')
        return redirect('course_list')

    if request.method == 'POST':
        # Handle user creation
        if 'first_name' in request.POST and 'email' in request.POST:
            # ...existing code...
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            student_id = request.POST.get('student_id')
            role = request.POST.get('role')
            password = request.POST.get('password', 'changeme123')
            if not all([first_name, last_name, email, student_id, role]):
                messages.error(request, 'All required fields must be filled.')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'A user with this email already exists.')
                else:
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        student_id=student_id,
                        role=role,
                        password=password
                    )
                    user.is_active = True
                    user.save()
                    messages.success(request, f'User {first_name} {last_name} created successfully!')
        # Handle student enrollment
        elif 'student_id' in request.POST and 'course_id' in request.POST:
            # ...existing code...
            try:
                student = User.objects.get(id=request.POST.get('student_id'), role='student')
                course = Course.objects.get(id=request.POST.get('course_id'))
                student.enrolled_courses.add(course)
                messages.success(request, f"Enrolled {student.get_full_name()} in {course.title}.")
            except Exception as e:
                messages.error(request, f"Error enrolling student: {e}")
        # Handle user edit
        elif 'edit_user_id' in request.POST:
            # ...existing code...
            try:
                user = User.objects.get(id=request.POST.get('edit_user_id'))
                user.first_name = request.POST.get('edit_first_name')
                user.last_name = request.POST.get('edit_last_name')
                user.email = request.POST.get('edit_email')
                user.username = request.POST.get('edit_email')
                user.student_id = request.POST.get('edit_student_id')
                user.role = request.POST.get('edit_role')
                user.is_active = 'edit_is_active' in request.POST
                user.save()
                messages.success(request, f"User {user.get_full_name()} updated successfully!")
            except Exception as e:
                messages.error(request, f"Error updating user: {e}")
        # Handle assigning courses to instructor
        elif request.POST.get('assign_instructor_courses') == '1':
            instructor_id = request.POST.get('instructor_id')
            course_ids = request.POST.getlist('course_ids')
            try:
                instructor = User.objects.get(id=instructor_id, role='instructor')
                # Unassign instructor from all courses first
                Course.objects.filter(instructor=instructor.get_full_name()).update(instructor='')
                # Assign selected courses to this instructor
                for cid in course_ids:
                    course = Course.objects.get(id=cid)
                    course.instructor = instructor.get_full_name()
                    course.save()
                messages.success(request, f"Assigned {len(course_ids)} course(s) to {instructor.get_full_name()}.")
            except Exception as e:
                messages.error(request, f"Error assigning courses: {e}")

    users = User.objects.all().order_by('last_name', 'first_name')
    courses = Course.objects.all().order_by('title')
    # Prepare user data for JSON serialization
    user_json = [
        {
            'id': u.id,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'email': u.email,
            'student_id': u.student_id,
            'role': u.role,
            'is_active': u.is_active,
        }
        for u in users
    ]

    # Build instructor-to-courses mapping for the UI
    instructor_courses = {}
    for user in users:
        if user.role == 'instructor':
            instructor_courses[str(user.id)] = [course.id for course in courses if course.instructor == user.get_full_name()]

    import json
    instructor_courses_json = json.dumps(instructor_courses)

    return render(request, 'user_management.html', {
        'users': users,
        'courses': courses,
        'user_json': user_json,
        'instructor_courses_json': instructor_courses_json,
    })
