from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

app_name = 'front'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('login/',csrf_exempt(views.LoginView.as_view()),name='login'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('send_sms/', csrf_exempt(views.SendSmsView.as_view()), name='send_sms'),
    path('d_login/', csrf_exempt(views.DynamicLogin.as_view()), name='d_login'),
    path('register/', csrf_exempt(views.RegisterView.as_view()), name='register'),
    path('info/', views.UserCenterInfoView.as_view(), name='info'),
    path('image/upload/', views.UploadImageView.as_view(), name='image'),
    path('update/pwd/', views.ChangePwdView.as_view(), name='update_pwd'),
    path('update/mobile/', views.ChangeMobileView.as_view(), name='update_mobile'),
    path('mycourse/', views.MyCourseView.as_view(), name='mycourse'),
    path('mymessage/', views.MyMessageView.as_view(), name='mymessage'),
]
