from rest_framework import serializers
from posts.models import Post
from unicodedata import category
from users.api.serializers import UserSerializer
from categories.api.serializers import CategorySerializer
from users.models import User
from categories.models import Category

class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model = Post
        fields = ['title', 'content', 'slug', 'user', 'miniature', 'created_at', 'published', 'category']

class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = ['id','title', 'content', 'slug', 'user', 'miniature', 'created_at', 'published', 'category']



class PostListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    category = CategorySerializer()
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'slug', 'user', 'miniature', 'created_at', 'published', 'category']