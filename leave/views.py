from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from employee.models import CustomUser
from leave.models import Leaves
from Email.email_sender import SendEmail
from employee.views import decode_token
from rest_framework.decorators import api_view
# Create your views here.

class AddLeave(APIView):
    permission_classes = [IsAuthenticated]

    # To add leave by employee
    def post(self, request):
        try:
            token = decode_token(request)
            if token:
                user_id = token.get('user_id') 
                if user_id is not None:   
                    user = CustomUser.objects.get(pk=user_id)
                else:
                    return JsonResponse({'error': 'Invalid or missing user_id in token'}, status=400)
            else:
                return JsonResponse({'error': 'Authorization header missing'}, status=400)  
                           
            serializer = LeavesSerializer(data = request.data)
            if serializer.is_valid():
                manager_email= user.manager
                
                leave=serializer.save(employee=user)
                print(serializer.data)
                print("llll",leave)

                default_leave_text = Leaves._meta.get_field('leave_status_text').default
                SendEmail(str(manager_email), leave)
                return JsonResponse({'message' : 'Leave added successfully'},status=200) 
            else:
                return JsonResponse({"error": serializer.errors},status=400)  
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Unauthorized user'}, status=401)   
        except Exception as error:
            return JsonResponse({"error": str(error)},status=500)
        
# manager can retrieve all pending leaves
class ViewPendingLeaves(APIView): 
    permission_classes=[IsAuthenticated]
      
    def get(self, request):
        try:
            # decode token
            token = decode_token(request)
            if token:
                user_id = token.get('user_id') 
                if user_id is not None:   
                    user = CustomUser.objects.get(pk=user_id)
                else:
                    return JsonResponse({'error': 'Invalid or missing user_id in token'}, status=400)
            else:
                return JsonResponse({'error': 'Authorization header missing'}, status=400)
              
            # authenticate manager or not
            if user.is_manager:
                leaves = Leaves.objects.filter(leave_status=0)  
                if not leaves:
                    return JsonResponse({"message": "No pending leaves found"}, status=404)
                serializer = AllLeavesSerializer(leaves, many=True)
                return JsonResponse({"Leaves": serializer.data}, status= 200)
            else:
                return JsonResponse({"message": "Unauthorized to perform this task"}, status=401)
        except CustomUser.DoesNotExist:
            return JsonResponse({"message": "User does not exist"}, status=404)
        except Exception as error:
            print("error : ",error)
            return JsonResponse({"error": str(error)}, status=500)
        

# To approve/reject leave by  manager only
class ApproveRejectLeave(APIView):
    def put(self, request):
        try:
            # Decode token
            token = decode_token(request)
            if token:
                user_id = token.get('user_id') 
                if user_id is not None:   
                    user = CustomUser.objects.get(pk=user_id)
                else:
                    return JsonResponse({'error': 'Invalid or missing user_id in token'}, status=400)
            else:
                return JsonResponse({'error': 'Authorization header missing'}, status=400)
            
            # authenticate manager or not
            if user.is_manager:
                serializer = UpdateLeaveSerializer(data = request.data)

                if serializer.is_valid():
                    leave_id = serializer.validated_data.get('leave_id')
                    leave_status = serializer.validated_data.get('leave_status')

                    leave = Leaves.objects.get(pk=leave_id)                       
                    employee = CustomUser.objects.get(email=leave.employee)
                    manager_id = employee.manager_id                       

                    # Check manager aprroving leave is same as manager of employee applied leave
                    if manager_id==user_id:
                        if leave_status==1:
                            leave.leave_status = 1
                            leave.save()
                        elif leave_status==3:
                            leave.leave_status = 3
                            leave.save()
                        else:
                            return JsonResponse({"message" : "Invalid status code"}, status=400)
                        SendEmail(str(leave.employee), leave)
                        print("from update",leave.leave_status)                       
                        return JsonResponse({"message" : "Leave status updated"}, status=200)
                    else:
                        return JsonResponse({"message" : "Don't have permission to perform this task"}, status=401)
                else:
                    return JsonResponse({"error": serializer.errors},status=400)
            else:
                return JsonResponse({"message": "Unauthorized to perform this task"}, status=401)
        except Leaves.DoesNotExist:
                        return JsonResponse({"error" : "Leave does not exist"}, status=404)
        except CustomUser.DoesNotExist:
            return JsonResponse({"message": "User does not exist"}, status=404)
        except Exception as error:
            return JsonResponse({"error": str(error)},status=500)
        
        

# To delete the leave   
class DeleteLeave(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self, request, leave_id):
        try:
            leave = Leaves.objects.get(pk=leave_id)
            
            if leave.leave_status == 0:
                leave.leave_status=7
                leave.save()
                SendEmail(str(leave.employee), leave)
                leave.delete()
                return JsonResponse({"message" : "Leave delete successfully"}, status=200)

            elif leave.leave_status==2 or leave.leave_status==4:
                leave.leave_status=5
                leave.save()
                SendEmail(str(leave.employee), leave)          
                return JsonResponse({"message" : "Leave delete successfully"}, status=200)
        
        except Leaves.DoesNotExist:
            return JsonResponse({"error" : "Leave does not exist"}, status=404)    
        except Exception as error:
            return JsonResponse({"error": str(error)},status=500)


# To retrieve leaves of specific emloyee
class ViewEmployeeLeaves(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        try:
            token = decode_token(request)
            if token:
                user_id = token.get('user_id') 
                if user_id is not None:     
                    employee = CustomUser.objects.get(pk=user_id)   
                else:
                    return JsonResponse({'error': 'Invalid or missing user_id in token'}, status=400)
            else:
                return JsonResponse({'error': 'Authorization header missing'}, status=400)
            
            leaves = Leaves.objects.filter(employee=employee).order_by('-from_date')

            if not leaves:
                return JsonResponse({"message": "No leaves found for this employee"}, status=404)
            
            serializer = AllLeavesSerializer(leaves , many=True)
            
            return JsonResponse({'Leaves' : serializer.data},status=200)  
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)  
        except Exception as error:
            return JsonResponse({"error": str(error)},status=500)










