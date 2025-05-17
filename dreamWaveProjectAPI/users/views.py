from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email, password=password)
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Geçersiz e-posta veya şifre.'}, status=status.HTTP_401_UNAUTHORIZED)


class UpdateUserAPIView(APIView):
    def put(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'Kullanıcı bulunamadı.'}, status=status.HTTP_404_NOT_FOUND)

        username = request.data.get('username')
        password = request.data.get('password')

        if username:
            user.username = username
        if password:
            user.password = password

        user.save()

        return Response({
            'message': 'Kullanıcı bilgileri başarıyla güncellendi.',
            'id': user.id,
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_200_OK)


class CurrentUserAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get(self, request):
        if request.user.is_authenticated:
            return Response({
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email
            }, status=status.HTTP_200_OK)
        else:
            return Response({'user': None}, status=status.HTTP_401_UNAUTHORIZED)