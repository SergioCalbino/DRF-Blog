from comments.models import Comment
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from comments.api.serializers import CommentListSerializer, CommentCreateSerializer, CommentDetailSerializer
from comments.api.permissions import IsOwnerOrStaff

class CommentListApiView(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentListSerializer(comments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CommentCreateApiView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        print(request.user)
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response({'message': 'Error to create a comment'}, status=status.HTTP_400_BAD_REQUEST)


class CommentUpdateApiView(APIView):
    permission_classes = [IsOwnerOrStaff]  # Usar el permiso modificado

    def get(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response({'message': 'Comment Does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentDetailSerializer(comment)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


    def put(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)  # Obtener el comentario
        except Comment.DoesNotExist:
            return Response({'message': 'Comment Does not exist'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, comment)  # Verificar permisos

        # Si el comentario existe y el usuario tiene permisos, proceder con la actualización
        serializer = CommentDetailSerializer(comment, data=request.data, partial=True)  # Permite actualización parcial
        if serializer.is_valid(raise_exception=True):
            serializer.save()  # Guardar los cambios en el comentario
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response({'message': 'Comment Does not exist'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, comment)
        comment.delete()
        return Response({'message': 'Comment has been deleted'}, status=status.HTTP_204_NO_CONTENT)



