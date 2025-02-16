from rest_framework import serializers
from comments.models import Comment
from users.models import User
from posts.models import Post
from users.api.serializers import UserSerializer
from posts.api.serializers import PostListSerializer

class CommentListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    post = PostListSerializer()
    class Meta:
        model = Comment
        fields = ['id','content','created_at', 'user', 'post']


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    class Meta:
        model = Comment
        fields = ['content', 'user', 'post']


class CommentDetailSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    class Meta:
        model = Comment
        fields = ['content', 'user', 'post', 'created_at']