from django.shortcuts import render

# Create your views here.

def manage_student(request):
    return render(request, 'teacher_homepage/manage_student.html')

def add_student(request):
    return render(request, 'teacher_homepage/add_student.html')

def manage_chapter(request):
    return render(request, 'teacher_homepage/manage_chapter.html')

def add_chapter(request):
    return render(request, 'teacher_homepage/add_chapter.html')

def detail_chapter(request):
    return render(request,'teacher_homepage/detail_chapter.html')
 
def edit_chapter(request):
    return render(request,'teacher_homepage/edit_chapter.html')
