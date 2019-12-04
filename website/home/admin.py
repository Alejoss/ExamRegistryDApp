from django.contrib import admin

# Register your models here.
from home.models import Exam, Professor

admin.site.register(Exam)
admin.site.register(Professor)
