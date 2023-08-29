from django.shortcuts import render
from rest_framework.views import APIView 
from django.http import JsonResponse
from rest_framework import status
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
# Create your views here.


class RegisterUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = CustomUserSerializer(data = request.data)

            if serializer.is_valid():
                user = serializer.save()
                return JsonResponse({'message' : 'Registration successful'},status=200) 
            else:
                return JsonResponse({"error": serializer.errors},status=400)     
        except Exception as error:
            return JsonResponse({"error": str(error)},status=500)


def generate_jwt_token(user):
    payload = {
        "token_type": "access",
        'user_id': user.id,
        'email': user.email,
        'is_manager': user.is_manager,  # Add is_manager to payload
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token.decode('utf-8')


class LoginUser(APIView):
    def post(self, request):
        try:            
            serializer = LoginSerializer(data = request.data)
                        
            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                password = serializer.validated_data.get('password') 
                                      
                user = authenticate(request=request, username=email, password=password)
                
                if user is not None:
                    jwt_token = generate_jwt_token(user)
                    refresh = RefreshToken.for_user(user)
                    return JsonResponse({"refresh": str(refresh),
                                        "access": str(refresh.access_token),
                                        "message": "Login successful", 
                                        "is_manager": user.is_manager,
                                        "jwt_token":jwt_token
                                        }, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({"message": "Invalid credentials."}, status=401)
            return JsonResponse({"message": serializer.errors},status=400)
       
        except Exception as error:
            print(error)
            return JsonResponse({"error": str(error)},status=500)



