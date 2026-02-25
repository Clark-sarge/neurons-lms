"""
Django management command to create test accounts for the LMS.
Run: python manage.py seed_test_accounts
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from lms_app.models import User, Course


# Default password for all test accounts (change in production!)
TEST_PASSWORD = "testpass123"

TEST_ACCOUNTS = [
    # Admin
    {
        "username": "admin@neurons-lms.test",
        "email": "admin@neurons-lms.test",
        "first_name": "Alex",
        "last_name": "Admin",
        "student_id": "ADMIN001",
        "role": User.ADMIN,
        "is_staff": True,
        "is_superuser": True,
    },
    # Instructors
    {
        "username": "instructor@neurons-lms.test",
        "email": "instructor@neurons-lms.test",
        "first_name": "Jordan",
        "last_name": "Instructor",
        "student_id": "INST001",
        "role": User.INSTRUCTOR,
    },
    {
        "username": "instructor2@neurons-lms.test",
        "email": "instructor2@neurons-lms.test",
        "first_name": "Sam",
        "last_name": "Coach",
        "student_id": "INST002",
        "role": User.INSTRUCTOR,
    },
    # Students
    {
        "username": "student@neurons-lms.test",
        "email": "student@neurons-lms.test",
        "first_name": "Casey",
        "last_name": "Student",
        "student_id": "STU001",
        "role": User.STUDENT,
    },
    {
        "username": "student2@neurons-lms.test",
        "email": "student2@neurons-lms.test",
        "first_name": "Morgan",
        "last_name": "Learner",
        "student_id": "STU002",
        "role": User.STUDENT,
    },
    {
        "username": "student3@neurons-lms.test",
        "email": "student3@neurons-lms.test",
        "first_name": "Riley",
        "last_name": "Demo",
        "student_id": "STU003",
        "role": User.STUDENT,
    },
]


class Command(BaseCommand):
    help = "Creates test accounts (admin, instructors, students) for development/demo. Skips users that already exist."

    def add_arguments(self, parser):
        parser.add_argument(
            "--with-course",
            action="store_true",
            help="Also create a sample course and assign the first instructor; enroll first two students.",
        )
        parser.add_argument(
            "--password",
            type=str,
            default=TEST_PASSWORD,
            help=f"Password for all test accounts (default: {TEST_PASSWORD})",
        )

    def handle(self, *args, **options):
        password = options["password"]
        with_course = options["with_course"]
        created_users = []
        skipped = []

        for data in TEST_ACCOUNTS:
            username = data["username"]
            if User.objects.filter(username=username).exists():
                skipped.append(username)
                continue
            user = User.objects.create_user(
                username=username,
                email=data["email"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                student_id=data["student_id"],
                role=data["role"],
                password=password,
            )
            if data.get("is_staff"):
                user.is_staff = True
            if data.get("is_superuser"):
                user.is_superuser = True
            user.is_active = True
            user.save()
            created_users.append(f"{user.get_full_name()} ({user.role})")

        if created_users:
            self.stdout.write(
                self.style.SUCCESS(f"Created {len(created_users)} user(s): {', '.join(created_users)}")
            )
        if skipped:
            self.stdout.write(
                self.style.WARNING(f"Skipped (already exist): {', '.join(skipped)}")
            )
        if not created_users and not skipped:
            self.stdout.write(self.style.WARNING("No test accounts defined."))

        if with_course:
            self._create_sample_course()

        self.stdout.write(
            self.style.SUCCESS(
                f"\nTest accounts use password: {password}\n"
                "See README.md for the full list of test accounts."
            )
        )

    def _create_sample_course(self):
        from lms_app.models import User

        # Get first instructor and first two students by email
        instructor = User.objects.filter(role=User.INSTRUCTOR).first()
        students = list(User.objects.filter(role=User.STUDENT).order_by("id")[:2])

        if not instructor:
            self.stdout.write(
                self.style.WARNING("--with-course: No instructor found; skipping course creation.")
            )
            return

        code = "NEURONS-101"
        if Course.objects.filter(code=code).exists():
            self.stdout.write(
                self.style.WARNING(f"--with-course: Course {code} already exists; skipping.")
            )
            return

        now = timezone.now()
        year = now.year
        semester = "Spring" if now.month <= 6 else "Fall"
        course = Course.objects.create(
            title="Introduction to Neurons LMS",
            code=code,
            description="A sample course for testing the learner-centric LMS.",
            instructor=instructor.get_full_name(),
            semester=semester,
            year=year,
        )
        for s in students:
            s.enrolled_courses.add(course)
        self.stdout.write(
            self.style.SUCCESS(
                f"Created sample course '{course.title}' ({course.code}), "
                f"instructor: {instructor.get_full_name()}, "
                f"enrolled: {len(students)} student(s)."
            )
        )
