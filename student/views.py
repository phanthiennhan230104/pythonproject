from django.shortcuts import render

def learning_view(request):
    return render(request, 'student_homepage/Learning.html')

def ide_view(request):
    return render(request, 'student_homepage/IDEonline.html')

def practice_view(request):
    return render(request, 'student_homepage/practice.html')