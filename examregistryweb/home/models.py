from django.db import models
from django.contrib.auth.models import User


class Exam(models.Model):
    questions = models.CharField(max_length=10000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Professor(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
