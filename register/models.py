from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.hashers import make_password
from datetime import date
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from social_books import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

# class CustomUserManager(BaseUserManager):
#     def create_superuser(self, username, email=None, password=None, fullname=None, dob=None, age=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self._create_user(username, email, password, fullname=fullname, dob=dob, age=age, **extra_fields)

#     def _create_user(self, username, email, password=None, fullname=None, dob=None, age=None, **extra_fields):
#         if not username:
#             raise ValueError('The Username field must be set.')

#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)

#         # Hash the password
#         if password:
#             password = make_password(password)

#         # Create and save the user
#         user = self.model(username=username, email=email, fullname=fullname, dob=dob, age=age, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user


class CustomUser(AbstractUser):
    # GENDER_CHOICES = (
    #     ('M', 'Male'),
    #     ('F', 'Female')
    # )
    # gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    # class Meta:
    #     swappable = 'AUTH_USER_MODEL'

    fullname = models.CharField(max_length=255)
    visibility = models.BooleanField()
    today = date.today().year
    dob = models.IntegerField(
        validators=[
            MaxValueValidator(2023, message='Number should be maximum 4 digits.'),
            MinValueValidator(1900, message='Number should be minimum 0.')
        ]
    )
    age = models.IntegerField(
        validators=[
            MaxValueValidator(0, message='Number should be maximum 4 digits.'),
            MinValueValidator(100, message='Number should be minimum 0.')
        ]
    )
    # # Any additional fields or methods specific to your user model

    # objects = CustomUserManager()

    def __str__(self):
        return self.username

# from django.contrib.auth.models import AbstractUser
# from django.core.validators import MaxValueValidator, MinValueValidator
# from django.db import models
# from datetime import date
# from django.contrib.auth.hashers import make_password
# from django.core.validators import MaxValueValidator, MinValueValidator


# class CustomUser(AbstractUser):
#     GENDER_CHOICES = (
#         ('M', 'Male'),
#         ('F', 'Female')
#     )
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
#     fullname = models.CharField(max_length=255)
#     visibility = models.BooleanField(default=False)
#     dob = models.IntegerField(
#         validators=[
#             MaxValueValidator(2023, message='Number should be maximum 4 digits.'),
#             MinValueValidator(1900, message='Number should be minimum 0.')
#         ]
#     )
#     age = models.IntegerField(
#         validators=[
#             MaxValueValidator(0, message='Number should be maximum 4 digits.'),
#             MinValueValidator(100, message='Number should be minimum 0.')
#         ]
#     )
#     def save(self, *args, **kwargs):
#         if not self.id:
#             self.password = make_password(self.password)
#         super().save(*args, **kwargs)
#     def __str__(self):
#         return self.username

class UploadedFiles(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    visibility = models.BooleanField(default=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    year_published = models.PositiveIntegerField()
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=255)
    # username = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = 'uploaded_files')

    def __str__(self):
        return self.title

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
