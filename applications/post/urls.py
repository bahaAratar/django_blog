from django.urls import path, include
from applications.post.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register('comment', CommentViewSet, basename='comment')
router.register('comment', CommentModelViewSet)
router.register('', PostModelViewSet)


urlpatterns = [
    # path('', PostListAPIView.as_view()),
    # path('create/', PostCreateAPIView.as_view()),
    # path('update/<int:pk>/', PostUpdateAPIView.as_view()),
    # # path('detail/<int:id>/', PostDeatailAPIView.as_view()),
    # # path('delete/<int:pk>/', PostDeleteAPIView.as_view()),

    path('', include(router.urls)),
    # path('', PostListCreateAPIView.as_view()),
    # path('<int:pk>/', PostDetailDeleteUpdataAPIView.as_view()),

    path('add/image/', CreateImageAPIView.as_view()),
    # path('comments/', CommentViewSet.as_view({'get': 'list'})),
]