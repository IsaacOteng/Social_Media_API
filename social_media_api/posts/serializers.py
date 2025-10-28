from .models import Post, Comment
from django.contrib.auth import get_user_model
from rest_framework import serializers

# posts/serializers.py
from rest_framework import serializers
from .models import Post
from .spotify import get_track_info




class PostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'post_type', 'album_cover_url', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        author = getattr(request, 'user', None)
        if not author or not author.is_authenticated:
            raise serializers.ValidationError("Authentication required to create posts.")

        post_type = validated_data.get('post_type', 'text')
        if post_type == 'music':
            track_id = validated_data.get('track_id')
            if not track_id:
                raise serializers.ValidationError("track_id is required for music posts.")
            track_data = get_track_info(track_id)
            validated_data['title'] = track_data['song_title']
            validated_data['album_cover_url'] = track_data['album_cover_url']

        return Post.objects.create(author=author, **validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.post_type == 'text':
            representation.pop('album_cover_url', None)
        return representation




class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        author = getattr(request, 'user', None)
        if not author or not author.is_authenticated:
            raise serializers.ValidationError("Authentication required to create comments.")
        return Comment.objects.create(author=author, **validated_data)
