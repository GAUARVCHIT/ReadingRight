from django.urls import path
from . import views

urlpatterns = [
    path('singleUserPost/',views.PostsListAPIView.as_view()),
    path('singleUserPost/<int:id>',views.PostsDetailAPIView.as_view()),
    path('posts/',views.TotalPostAPIView.as_view(),name="posts"),
]