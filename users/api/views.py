from logging import raiseExceptions

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.utils import IntegrityError
from users.api.serializers import UserRegisterSerializer, UserSerializer, UserUpdateSerializer
from users.models import User
from rest_framework.permissions import IsAuthenticated

#Registro un usuario

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        print(serializer)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer.save()
            return Response(data={'message': 'User created successfully', 'post': serializer.data},
                            status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response(data={'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={"errors": {"detail": str(e)}}, status=status.HTTP_400_BAD_REQUEST)

#Loguea al usuario. Ver routes con el token. Se debe enviar un Bearer para loguearse
class UserView(APIView):
    permission_classes = [IsAuthenticated]

    #Loguea
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    #actualiza
    def put(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserUpdateSerializer(user, request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class UserShowAll(APIView):

    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

