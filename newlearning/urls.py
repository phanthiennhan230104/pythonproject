from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin_homepage/', include('admin.urls')),
    path('', include('authentication.urls')),
    path('student/', include('student.urls')),
    path('teacher/', include('teacher.urls', )),
    path('ai/', include(('ai.urls', 'ai'), )),

   

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
