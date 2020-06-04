from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
app_name = 'org'

urlpatterns = [
    path('',views.OrgView.as_view(),name='org'),
    path('ask/',csrf_exempt(views.AskView.as_view()),name='ask'),
    path('<int:org_id>/',views.OrgHomeView.as_view(),name='home'),
    path('<int:org_id>/teacher/',views.OrgTeacherView.as_view(),name='teacher'),
    path('<int:org_id>/desc/',views.OrgDescView.as_view(),name='desc'),
    path('<int:org_id>/course/',views.OrgCourseView.as_view(),name='course'),
    path('teacher/',views.TeacherView.as_view(),name='teacher'),
    path('teacher/detail/<int:t_id>',views.TeacherDetailView.as_view(),name='teacher_detail'),
]