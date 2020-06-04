from django.urls import path
from . import views

app_name = 'course'

urlpatterns = [
    path('',views.CourseView.as_view(),name='course'),
    path('<int:course_id>/',views.CourseDetailView.as_view(),name='detail'),
    path('<int:course_id>/lesson/',views.CourseLessonView.as_view(),name='lesson'),
    path('<int:course_id>/comments/',views.CourseCommentsView.as_view(),name='comments'),
    path('<int:course_id>/lesson/<int:video_id>',views.CourseVideoView.as_view(),name='video')
]