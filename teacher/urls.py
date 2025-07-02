from django.contrib import admin
from django.urls import path
from . import views
app_name = 'teacher'
urlpatterns = [
    path('manage_student/', views.manage_student, name='manage_student'),   
    path('add_student/', views.add_student, name='add_student'),
    path('manage_chapter/',views.manage_chapter, name="manage_chapter"),
    path('add_chapter/',views.add_chapter, name="add_chapter"),
    path('detail_chapter/',views.detail_chapter, name = "detail_chapter"),
    path('edit_chapter/',views.edit_chapter, name = "edit_chapter")
]