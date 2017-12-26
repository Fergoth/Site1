"""courseSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from . import views
from course_work.views import CourseView,NewCourseView,\
    AcceptRequestView,DeleteRequestView,ChooseYourPerformerView,\
    CompleteCourseView,upload_file,download,RdyCourseView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_user),
    path('register/', views.register_user, name='register'),
    path('', views.main_page,name ='main'),
    path('course/', CourseView.as_view(), name ='course'),
    path('course/new', NewCourseView.as_view(), name='new_course'),
    path('course/accept/<int:pk>', AcceptRequestView.as_view(), name='accept_request'),
    path('course/delete/<int:pk>',DeleteRequestView.as_view(), name='delete_request'),
    path('course/choose_performer/<int:pk>/<int:performer_id>',ChooseYourPerformerView.as_view(), name ='choose_performer'),
    path('complete_course',CompleteCourseView.as_view(), name ='complete_course'),
    path('rdy_course',RdyCourseView.as_view(), name ='rdy_course'),
    path('upload_file/<int:pk>',upload_file,name='upload_file'),
    re_path('download/(?P<path>.*)$',download,name ='download'),
]
urlpatterns+=static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)
