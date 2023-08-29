from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from employee.models import CustomUser
# Create your views here.

class AddLeave(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    # To add leave by employee
    def post(self, request):
        try:                 
            serializer = LeavesSerializer(data = request.data)
            if serializer.is_valid():
                user_id=serializer.validated_data.get('employee')
                employee_details = CustomUser.objects.get(email=user_id)
                serializer.save(employee=employee_details)
                return JsonResponse({'message' : 'Leave added successfully'},status=200) 
            else:
                return JsonResponse({"error": serializer.errors},status=400)  
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Unauthorized user'}, status=401)   
        except Exception as error:
            return JsonResponse({"error": str(error)},status=500)
