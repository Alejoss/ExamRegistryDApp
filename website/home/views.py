from django.shortcuts import render
import hashlib
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
from home.models import Exam, Professor


def home(request):
    template = "home.html"
    professors = Professor.objects.all()
    for p in professors:
        if not p.exam:
            e = Exam.objects.create(hash="na")
            p.exam = e
            p.save()

    context = {'professors': professors}
    return render(request, template, context)


def exams_index(request, exam_id):
    template = "exams.html"
    exam = Exam.objects.get(id=exam_id)
    professor = Professor.objects.get(user=request.user)
    context = {'exam': exam, 'professor': professor}
    return render(request, template, context)


def edit_exam(request):
    template = "edit_exam.html"
    if request.method == "POST":
        q1 = request.POST.get("question1")
        q2 = request.POST.get("question2")
        q3 = request.POST.get("question3")
        q4 = request.POST.get("question4")
        q5 = request.POST.get("question5")
        q6 = request.POST.get("question6")
        q7 = request.POST.get("question7")
        q8 = request.POST.get("question8")
        q9 = request.POST.get("question9")
        q10 = request.POST.get("question10")
        professor = Professor.objects.get(user=request.user)
        exam = professor.exam
        exam.q1 = q1
        exam.q2 = q2
        exam.q3 = q3
        exam.q4 = q4
        exam.q5 = q5
        exam.q6 = q6
        exam.q7 = q7
        exam.q8 = q8
        exam.q9 = q9
        exam.q10 = q10
        exam.hash = hashlib.sha3_256((q1+q2+q3+q4+q5+q6+q7+q8+q9+q10).encode('utf-8')).hexdigest()
        exam.save()
        return redirect('exams', exam_id=professor.exam.id)

    else:
        # Get the professor actual exam
        if request.user.is_authenticated:
            current_user = request.user
            professor = Professor.objects.get(user=current_user)
            return render(request, template, {'professor': professor, 'exam': professor.exam})
        else:
            return HttpResponse("You need to login to create an exam")
