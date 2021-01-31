from django.urls import path
from . import views

urlpatterns = [
    path('singleUser/',views.PostsListAPIView.as_view()),
    path('singleUser/<int:id>',views.PostsDetailAPIView.as_view()),
    path('posts/',views.TotalPostAPIView.as_view(),name="posts"),
]