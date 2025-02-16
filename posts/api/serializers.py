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

    # def create(self, validated_data):
    #     user_data = validated_data.get('user')
    #     category_data = validated_data.get('category')
    #
    #     user = User.objects.get(**user_data)
    #     category = Category.objects.get(**category_data)
    #
    #     post = Post.objects.create(user=user, category=category, **validated_data)
    #     return post

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