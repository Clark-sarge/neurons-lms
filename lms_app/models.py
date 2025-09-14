
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	STUDENT = 'student'
	INSTRUCTOR = 'instructor'
	ADMIN = 'admin'
	ROLE_CHOICES = [
		(STUDENT, 'Student'),
		(INSTRUCTOR, 'Instructor'),
		(ADMIN, 'Admin'),
	]
	role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)
	student_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
	enrolled_courses = models.ManyToManyField('Course', related_name='enrolled_students', blank=True)


class Course(models.Model):
	title = models.CharField(max_length=255)
	code = models.CharField(max_length=50, unique=True)
	description = models.TextField(blank=True)
	instructor = models.CharField(max_length=255)
	semester = models.CharField(max_length=100)
	year = models.IntegerField()
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)

	def __str__(self):
		return self.title

class Module(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
	title = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='submodules')
	available_from = models.DateTimeField(null=True, blank=True)
	available_until = models.DateTimeField(null=True, blank=True)
	is_published = models.BooleanField(default=False)

	def __str__(self):
		return self.title

class Content(models.Model):
	FILE = 'file'
	LINK = 'link'
	QUIZ = 'quiz'
	DISCUSSION = 'discussion'
	CONTENT_TYPE_CHOICES = [
		(FILE, 'File'),
		(LINK, 'Link'),
		(QUIZ, 'Quiz'),
		(DISCUSSION, 'Discussion'),
	]
	module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='contents')
	title = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
	file = models.FileField(upload_to='content_files/', null=True, blank=True)
	url = models.URLField(blank=True)
	time_limit = models.PositiveIntegerField(null=True, blank=True, help_text='Time limit in minutes for quizzes')
	max_attempts = models.PositiveIntegerField(null=True, blank=True)
	passing_score = models.PositiveIntegerField(null=True, blank=True)
	show_correct_answers = models.BooleanField(default=False)
	randomize_questions = models.BooleanField(default=False)
	is_adaptive = models.BooleanField(default=False)
	allow_anonymous = models.BooleanField(default=False)
	moderated = models.BooleanField(default=False)
	max_posts_per_user = models.PositiveIntegerField(null=True, blank=True)
	available_from = models.DateTimeField(null=True, blank=True)
	available_until = models.DateTimeField(null=True, blank=True)
	is_published = models.BooleanField(default=False)

	def __str__(self):
		return self.title
