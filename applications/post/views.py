from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from ..feedback.models import *
from ..post.models import *
from ..post.serializers import *
from ..feedback.serilalizers import RatingSerilaizer
from ..post.permissions import IsOwner
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000

class PostModelViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwner]
    
    pagination_class = CustomPagination
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['owner', 'title']
    search_fields = ['title']
    ordering_fields = ['id', 'owner']

    @action(methods=['POST'], detail=True) # localhost:8000/api/v1/post/23/like/
    def like(self, request, pk, *args, **kwargs):
        user = request.user
        print(user)
        print(pk)
        like_obj, _ = Like.objects.get_or_create(owner=user, post_id=pk)
        like_obj.is_like = not like_obj.is_like
        like_obj.save()
        status = 'liked'

        if not like_obj.is_like:
            status = 'unlike'

        return Response({'status': status})

    @action(methods=['POST'], detail=True) # localhost:8000/api/v1/post/23/rating/
    def rating(self, request, pk, *args, **kwargs):
        serializers = RatingSerilaizer(data=request.data)
        serializers.is_valid(raise_exception=True)
        rating_obj, _ = Rating.objects.get_or_create(owner=request.user, post_id=pk)
        rating_obj.rating = serializers.data['rating']
        rating_obj.save()
        print(serializers.data)
        return Response(serializers.data)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CreateImageAPIView(generics.CreateAPIView):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer
    permission_classes = [IsAuthenticated]

class CommentViewSet(ViewSet):
    def list(self, request):
        comment = Comment.objects.all()
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)

class CommentModelViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = {IsAuthenticatedOrReadOnly}

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

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

# class PostListCreateAPIView(generics.ListCreateAPIView):
#     permission_classes = [IsOwner]

#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     pagination_class = CustomPagination
    
#     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#     filterset_fields = ['owner', 'title']
#     search_fields = ['title']
#     ordering_fields = ['id']

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     # queryset = queryset.filter(owner=2)
    #     filter_owner = self.request.query_params.get('owner')
    #     if filter_owner:

    #         queryset = queryset.filter(owner=filter_owner)

    #     return queryset

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)

# class PostDetailDeleteUpdataAPIView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsOwner]

#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
