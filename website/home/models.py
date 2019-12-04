from django.db import models

from django.db import models
from django.contrib.auth.models import User


class Exam(models.Model):
    hash = models.CharField(max_length=100)
    students_graduated = models.SmallIntegerField(default=0)
    q1 = models.CharField(max_length=250, blank=True)
    q2 = models.CharField(max_length=250, blank=True)
    q3 = models.CharField(max_length=250, blank=True)
    q4 = models.CharField(max_length=250, blank=True)
    q5 = models.CharField(max_length=250, blank=True)
    q6 = models.CharField(max_length=250, blank=True)
    q7 = models.CharField(max_length=250, blank=True)
    q8 = models.CharField(max_length=250, blank=True)
    q9 = models.CharField(max_length=250, blank=True)
    q10 = models.CharField(max_length=250, blank=True)


class Professor(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
