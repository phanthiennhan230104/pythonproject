from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager

from django.db import models
from django.conf import settings

class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_email_verified = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    def __str__(self):
        return self.user.email


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_email_verified', True)
        if 'role' not in extra_fields:
            role, _ = Role.objects.get_or_create(name='Admin', defaults={'description': 'Superuser'})
            extra_fields['role'] = role
        return self.create_user(username, email, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    created_date = models.DateTimeField(default=timezone.now)
    
    role = models.ForeignKey('Role', on_delete=models.CASCADE)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    is_staff = models.BooleanField(default=False) 
    is_email_verified = models.BooleanField(default=False)
    role = models.ForeignKey('Role', on_delete=models.CASCADE)

    objects = CustomUserManager()

    
    def __str__(self):
        return self.username

    class Meta:
        db_table = 'Users'  # <-- match với bảng đã có trong MySQL

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Roles'

from django.db import models
from django.utils import timezone

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    year = models.IntegerField(null=True, blank=True)
    teacher = models.ForeignKey('CustomUser', on_delete=models.CASCADE, db_column='teacher_id')

    class Meta:
        db_table = 'Courses'

class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Subjects'

class CourseSubject(models.Model):
    course_sub_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Course_Subject'
        unique_together = ('course', 'subject')

class Lesson(models.Model):
    lesson_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    course_sub = models.ForeignKey(CourseSubject, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Lessons'

class Assignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    due = models.DateTimeField(null=True, blank=True)
    file = models.CharField(max_length=255, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Assignments'

class Submission(models.Model):
    sub_id = models.AutoField(primary_key=True)
    student = models.ForeignKey('CustomUser', on_delete=models.CASCADE, db_column='student_id')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(default=timezone.now)
    point = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'Submissions'
        unique_together = ('student', 'assignment')

class CourseStudent(models.Model):
    cs_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey('CustomUser', on_delete=models.CASCADE, db_column='student_id')
    enrolled_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'Course_Student'
        unique_together = ('course', 'student')

class CourseFeedback(models.Model):
    cf_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey('CustomUser', on_delete=models.CASCADE, db_column='student_id')
    rating = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    submitted_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'Course_Feedback'
        unique_together = ('course', 'student')

class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, db_column='sender_id')
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_global = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'Notifications'

class NotificationUser(models.Model):
    noti_user_id = models.AutoField(primary_key=True)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'Notification_User'
        unique_together = ('notification', 'user')


