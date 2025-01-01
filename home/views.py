from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import LoginSerializer, RegisterSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

class RegisterUser(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            data = request.data
            serializer = RegisterSerializer(data = data)
            if not serializer.is_valid():
                return Response(serializer.errors)
            email = serializer.data['email']
            password = serializer.data['password']
            username = serializer.data['username']

            print(serializer.data)
            
            if(User.objects.filter(email = email)):
                return Response('Email already exists')
            
            User.objects.create_user(email=email, password=password, username=username)
            return Response('User created successfully')
            
        except Exception as err:
            print(err)
            return Response('Internal server error')

class LoginUser(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors)
            email = serializer.data['email']
            password = serializer.data['password']
            print(email, password)
            user = authenticate(email = email, password = password)

            if user is None:
                return Response('Incorrect email or password')

            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh' : str(refresh),
                'access' : str(refresh.access_token)
            })
        
        except Exception as err:
            print(err)
            return Response('Error occoured')

class ProtectedApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message' : 'This is a protected route', 'user' : request.user.username})
