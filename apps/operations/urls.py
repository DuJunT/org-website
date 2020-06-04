from django.urls import path
from . import views

app_name = 'op'

urlpatterns = [
    path('',views.AddFavView.as_view(),name='fav'),
    path('comment/',views.CommentView.as_view(),name='comment'),
]