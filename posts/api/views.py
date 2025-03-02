from posts.models import Post
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from posts.api.serializers import PostSerializer, PostListSerializer, PostDetailSerializer
from posts.api.permissions import IsAdminOrReadOnly, IsOwnerOrStaff
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from categories.models import Category
from posts.api.paginations import CustomPagination
from rest_framework.permissions import IsAuthenticated



# class PostApiViewSet(ModelViewSet):
#     permission_classes = [IsAdminOrReadOnly]
#     serializer_class = PostSerializer
#     queryset = Post.objects.filter(published=True)
#     lookup_field = 'slug'
#     filter_backends = [DjangoFilterBackend]
#     # filterset_fields = ['category']
#     filterset_fields = ['category__slug']

class PostListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()

        category = request.query_params.get('category')

        if category is not None:
            try:
                if category.isdigit():
                    if not Category.objects.filter(pk=category).exists():
                        return Response({'message': 'Category Does Not Exist (id)'}, status=status.HTTP_404_NOT_FOUND)
                    posts = posts.filter(category=category)
                else:
                    if not Category.objects.filter(slug=category).exists():
                        return Response({'message': 'Category Does Not Exist (slug)'}, status=status.HTTP_404_NOT_FOUND)
                    posts = posts.filter(category__slug=category)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        paginator = CustomPagination()
        paginator.page_size = 5
        paginated_post = paginator.paginate_queryset(posts, request)
        serializer = PostListSerializer(paginated_post, many=True)
        paginated_response = paginator.get_paginated_response(serializer.data).data

        # Construimos la respuesta con solo el array de posts
        response = Response(serializer.data, status=status.HTTP_200_OK)

        # Agregamos los headers con la información de paginación
        response["X-Total-Count"] = paginated_response["count"]  # Total de elementos
        print(f'Soy el x total count{response["X-Total-Count"]}')
        response["X-Next-Page"] = paginated_response["next"] if paginated_response["next"] else ""
        print(f'Soy el x next page {response["X-Next-Page"]}')
        response["X-Previous-Page"] = paginated_response["previous"] if paginated_response["previous"] else ""

        return response


class PostCreateView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def post(self, request):
        serializer = PostSerializer(data=request.data)

        if not serializer.is_valid():
            print(serializer.errors)
            return Response(data={'message': 'error to create Post', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST )
        serializer.save()
        return Response(data={'message': 'Post created successfully', 'post': serializer.data}, status=status.HTTP_201_CREATED)
        # return Response({'message': 'Error to create post'}, status=status.HTTP_400_BAD_REQUEST)

class PostDetailView(APIView):
    permission_classes = [IsAdminOrReadOnly, IsOwnerOrStaff]
    def get(self, request, slug):

        try:
            post = Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            return Response({'message': 'Slug does not exist'}, status=status.HTTP_404_NOT_FOUND)

        try:
            serializer = PostDetailSerializer(post)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except(TypeError, ValueError) as e:
            return Response({'error': f'Error during serialization: {str(e)}'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, slug):

        try:
            post = Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            return Response({'message': 'Slug does not exist'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, post)
        serializer = PostDetailSerializer(post, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data={'message': 'Post updated successfully', 'post': serializer.data}, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, slug):

        try:
            post = Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            return Response({'message': 'Slug does not exist'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, post)

        serializer = PostDetailSerializer(post, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):

        try:
            post = Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            return Response({'message': 'Slug does not exist'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, post)

        post.delete()
        return Response({'message': 'Post deleted successfully'}, status=status.HTTP_200_OK)






