from django.db import models


# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True, verbose_name="Subject Name")


class Teacher(models.Model):
    first_name = models.CharField(max_length=100, null=False, blank=False, verbose_name="First Name")
    last_name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Last Name")

    profile_picture = models.ImageField(upload_to='styles/images/teachers/%Y/%m/%d', blank=True)
    email = models.EmailField(max_length=200, null=False, blank=False, unique=True, verbose_name="Email")

    phone = models.CharField(max_length=100, null=False, blank=False, verbose_name="Phone")
    room_no = models.CharField(max_length=100, null=False, blank=False, verbose_name="Room No")

    subjects = models.ManyToManyField(Subject)
