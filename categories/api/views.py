from rest_framework.decorators import permission_classes
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from categories.models import Category
from categories.api.serializers import CategorySerializer, CategoryCreateSerializer, CategoryListSerializer, CategoryDetailSerializer
from categories.api.permissions import IsAdminOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CategoryApiViewSet(ModelViewSet):
    pass
#     permission_classes = [IsAdminOrReadOnly]
#     serializer_class = CategorySerializer
#     # queryset = Category.objects.all()
#     lookup_field = 'slug'
#
#     #filtrar sin sistema de filtros
#     queryset = Category.objects.filter(published=True)

    #filtrar con sistema de filtros
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['published']

class CategoryCreateApiView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def post(self, request):
        serializer = CategoryCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST )

class CategoryListApiView(APIView):
    def get(self, request):
        categories = Category.objects.all()

        published = request.query_params.get('published')
        if published is not None and published.lower() not in ['true', 'false']:
            return Response({'message': 'Invalid filter use true or false'})

        if published is not None:
            #Este filtro convierte la cadena a minuscula
            categories = categories.filter(published=(published.lower() == 'true'))

        serializer = CategoryListSerializer(categories, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)



class CategoryDetailView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, slug):

        # try:
        #     slug = str(slug)
        # except ValueError:
        #     return Response(
        #         {"detail": "Invalid slug format. Slug must be a string."},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return Response({'message': 'Category Does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategoryDetailSerializer(category)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, slug):
        # try:
        #     slug = int(slug)
        # except ValueError:
        #     return Response(
        #         {"detail": "Invalid ID format. ID must be a number."},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return Response({'message': 'Category Does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategoryDetailSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        # try:
        #     slug = int(slug)
        #
        # except ValueError:
        #     return Response({'message': 'Id must be a number'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = Category.objects.get(slug=slug)

        except Category.DoesNotExist:
            return Response({'message': 'ID must be a number'}, status=status.HTTP_404_NOT_FOUND)

        category.delete()
        return Response({'message': 'Category was deleted successfully'},status=status.HTTP_204_NO_CONTENT)


