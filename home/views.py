from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
# from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

# Create your views here.


class RegisterUser(APIView):
     def post(self, request):
        
        serializer = RegisterSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({"status": 403, "payload":serializer.errors, "message": "Something went wrong"})

        serializer.save()
        return Response({"status": 200, "payload": serializer.data, 
        "message":"You have been registered..."})


class LoginUser(APIView):
    def post(self, request):
        permission_classes = [AllowAny]
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.data['email'])
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                refresh = RefreshToken.for_user(user)
                return Response({'refresh': str(refresh),
                'access': str(refresh.access_token),  
                "status":200, 
                "message":"You have been logged in.."})
            else:
                return Response({"error": "Invalid email or password", "status":400})
        return Response({'errors':serializer.errors, 'status':400})
# from rest_framework.authentication import 


class StudentAPI(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request):
        student_objs = Student.objects.all()
        serializer= StudentSerializer(student_objs, many=True)
        return Response({"status": 200, "payload": serializer.data})

    def post(self, request):
        serializer= StudentSerializer(data= request.data)

        if not serializer.is_valid():
           return Response({"status": 403, "payload":serializer.errors, "message": "Something went wrong"})
     # print(data)

        serializer.save()
        return Response({"status": 200, "payload": serializer.data, "message":"You have been saved your data..."})


    def put(self, request):
        try:
            student_obj = Student.objects.get(id=request.data['id'])
            serializer = StudentSerializer(student_obj, data=request.data, partial=True)

            if not serializer.is_valid():
                return Response({"status": 403, "payload": serializer.errors, "message": "Something went wrong"})

            serializer.save()
            return Response({"status": 200, "payload": serializer.data, "message": "Data has been updated successfully"})
        except Student.DoesNotExist:
            return Response({'status': 404, 'message': 'Student not found'})
        except Exception as e:
            return Response({'status': 500, 'message': 'An error occurred: ' + str(e)})


    def patch(self, request):
        pos

    def delete(self, request):
        try:
            student_obj = Student.objects.get(id=request.data['id'])
            # serializer = StudentSerializer(student_obj, data=request.data)
            student_obj.delete()
            return Response({'status':200, 'message': 'your data has been deleted'})

        except Exception as e:
            print(e)
            return Response({'status': 403, 'message': "Invalid id"})    

            






# @api_view(['GET'])
# def home(request):
#     student_objs = Student.objects.all()
#     serializer= StudentSerializer(student_objs, many=True)
#     return Response({"status": 200, "payload": serializer.data})

# @api_view(['POST'])
# def post_student(request):
#     # data = request.data
#     serializer= StudentSerializer(data= request.data)

#     if not serializer.is_valid():
#         return Response({"status": 403, "payload":serializer.errors, "message": "Something went wrong"})
#     # print(data)

#     serializer.save()
#     return Response({"status": 200, "payload": serializer.data, "message":"You have been saved your data..."})


# @api_view(['PUT'])
# def update_student(request, id):
#     try:
#         student_obj = Student.objects.get(id=id)
#         serializer = StudentSerializer(student_obj, data=request.data)

#         if not serializer.is_valid():
#             return Response({"status": 403, "payload": serializer.errors, "message": "Something went wrong"})

#         serializer.save()
#         return Response({"status": 200, "payload": serializer.data, "message": "Data has been updated successfully"})
#     except Student.DoesNotExist:
#         return Response({'status': 404, 'message': 'Student not found'})
#     except Exception as e:
#         return Response({'status': 500, 'message': 'An error occurred: ' + str(e)})


# @api_view(['DELETE'])
# def delete_student(request, id):
#     try:
#         student_obj = Student.objects.get(id=id)
#         # serializer = StudentSerializer(student_obj, data=request.data)
#         student_obj.delete()
#         return Response({'status':200, 'message': 'your data has been deleted'})

#     except Exception as e:
#         print(e)
#         return Response({'status': 403, 'message': "Invalid id"})    

