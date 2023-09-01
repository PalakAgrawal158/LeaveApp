from django.shortcuts import render
from rest_framework.views import APIView 
from django.http import JsonResponse
from rest_framework import status
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_jwt.utils import jwt_decode_handler
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
# Create your views here.


class RegisterUser(APIView):   
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
        'exp': datetime.now() + timedelta(days=1)
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
                    # jwt_token = generate_jwt_token(user)
                    refresh = RefreshToken.for_user(user)
                    return JsonResponse({"refresh": str(refresh),
                                        "access": str(refresh.access_token),
                                        "message": "Login successful", 
                                        "is_manager": user.is_manager,
                                        # "jwt_token":jwt_token
                                        }, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({"message": "Invalid credentials."}, status=401)
            return JsonResponse({"message": serializer.errors},status=400)
       
        except Exception as error:
            print(error)
            return JsonResponse({"error": str(error)},status=500)


class DeleteUser(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
            user.delete()
            return JsonResponse({"message":"User Deleted"}, status=200)
        except CustomUser.DoesNotExist:
            return JsonResponse({"error":"User does not exist"}, status=404)
        

#To decode the jwt token 
def decode_token(request):
    try:
        header = request.headers.get('Authorization')

        if header and header.startswith('Bearer '):
            jwt_token = header.split(' ')[1]

            if jwt_token:
                payload =jwt_decode_handler(jwt_token)
                if payload is not None:
                    return payload 
                else:
                    print('Payload is not available')
                    return False      
            else:
                print('Token not found')
                return False
        else:
            print('JWT token not found in Authorization header')
            return False    
        
    except Exception as error:
                print('Error------>',error)
                return False



class ListEmployeesByManager(APIView):
    def get(self,request,manager_id):
        try:
            employees = CustomUser.objects.filter(manager=manager_id)
            if employees:
                serializer = CustomUserSerializer(employees, many=True)
                return JsonResponse({"data":serializer.data},status=200)
            else:
                return JsonResponse({"message":"No employees available with this manager"},status=404)
        except Exception as error:
            print(error)
            return JsonResponse({"error":str(error)},status=500)
