from django.shortcuts import render
from rest_framework import generics
from applications.post.models import Post
from applications.post.serializers import PostSerializer
# from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from applications.post.permissions import IsOwner
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


# class PostListAPIView(generics.ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

# class PostCreateAPIView(generics.CreateAPIView):
#     serializer_class = PostSerializer

# class PostUpdateAPIView(generics.UpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

# class PostDeleteAPIView(generics.DestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

# class PostDeatailAPIView(generics.RetrieveAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     lookup_field = 'id'

class PostListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsOwner]

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['owner', 'title']
    search_fields = ['title']
    ordering_fields = ['id']

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     # queryset = queryset.filter(owner=2)
    #     filter_owner = self.request.query_params.get('owner')
    #     if filter_owner:
    #         queryset = queryset.filter(owner=filter_owner)

    #     return queryset

class PostDetailDeleteUpdataAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner]

    queryset = Post.objects.all()
    serializer_class = PostSerializer