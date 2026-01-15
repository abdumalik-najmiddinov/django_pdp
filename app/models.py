from django.db import models
from django.contrib.auth.models import AbstractUser

class Course(models.Model):
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    course_name = models.CharField(max_length=200)
    about = models.TextField(default="", blank=True)
    age_limit = models.PositiveIntegerField(default=0)
    price = models.CharField(max_length=50, default="0")

    def __str__(self):
        return self.course_name


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    image = models.ImageField(upload_to='teachers/', blank=True, null=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True)
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    author = models.CharField(max_length=100, default='Admin')
    category = models.CharField(max_length=100, default='Web Design')
    comments_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title




from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email majburiy")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser is_staff=True bo‘lishi kerak.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser is_superuser=True bo‘lishi kerak.')
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email