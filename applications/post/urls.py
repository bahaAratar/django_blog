from django.urls import path
from applications.post.views import *


urlpatterns = [
    # path('', PostListAPIView.as_view()),
    # path('create/', PostCreateAPIView.as_view()),
    # path('update/<int:pk>/', PostUpdateAPIView.as_view()),
    # # path('detail/<int:id>/', PostDeatailAPIView.as_view()),
    # # path('delete/<int:pk>/', PostDeleteAPIView.as_view()),

    path('', PostListCreateAPIView.as_view()),
    path('<int:pk>/', PostDetailDeleteUpdataAPIView.as_view()),
]