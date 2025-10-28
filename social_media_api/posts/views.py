from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment, Like
from notifications.models import Notification
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from .permissions import IsAuthorOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .spotify import get_track_info


# Create your views here.


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at'] 


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionError('You can only edit your own comments.')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionError('You can only delete your own comments.')
        instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class =CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        # Save the comment first
        comment = serializer.save(author=self.request.user)
        
        # Create notification for the post author
        if comment.post.author != self.request.user:
            Notification.objects.create(
                recipient=comment.post.author,
                actor=self.request.user,
                verb='commented on your post',
                content_type=ContentType.objects.get_for_model(Post),
                object_id=comment.post.id
            )

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionError('You can only edit your own comments.')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionError('You can only delete your own comments.')
        instance.delete()


class FeedView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        following = user.following.all()
        posts = Post.objects.filter(author__in=following).order_by('-created_at')
        
        # Use the pagination class
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Number of posts per page
        paginated_posts = paginator.paginate_queryset(posts, request)
        
        serializer = PostSerializer(paginated_posts, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        post = get_object_or_404(Post, pk=pk)


        
        like, created = Like.objects.get_or_create(post=post, user=user)

        if not created:
            like.delete()
            return Response({'message': 'Post unliked'}, status=status.HTTP_200_OK)
        if post.author != user:
            Notification.objects.create(
                recipient = post.author,
                actor = user,
                verb = 'liked your post',
                content_type = ContentType.objects.get_for_model(Post),
                object_id = post.id
            )
        return Response({'message': 'Post liked'}, status=status.HTTP_201_CREATED)


