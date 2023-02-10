from django.shortcuts import render
from .serializers import SignUpSerializer,CustomUser
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .tokens import create_jwt_pair_for_user
from drf_yasg.utils import swagger_auto_schema

# Create your views here.



class SignUpView(generics.GenericAPIView):
    serializer_class=SignUpSerializer


    @swagger_auto_schema(
            operation_summary="Signing up a new user",
            operation_description="Signing up a new user"
    )
    def post(self,request:Request):
        data=request.data

        serializer = self.serializer_class(data=data)


        if serializer.is_valid():
            serializer.save()
            respones={
                "message":"User created successfully",
                "data":serializer.data
            }
            return Response(data=respones, status=status.HTTP_201_CREATED)
        

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):


    @swagger_auto_schema(
            operation_summary="Logins in a user",
            operation_description="Logins in a user with email and password"
    )
    def post(self,request:Request):
        email=request.data.get('email')
        password = request.data.get('password')


        user=authenticate(email=email,password=password)

        if user is not None:
            #generating tokens
            tokens = create_jwt_pair_for_user(user)

            response={
                'message':'Login in successfully',
                'token': tokens
            }

            return Response(data=response,status=status.HTTP_200_OK)
        

        return Response(data={'error':'invalid email or password'})


    @swagger_auto_schema(
            operation_summary="Get request info",
            operation_description="This shows the request info"
    )
    def get(self,request:Request,format=None):
        
        content={
            "user":str(request.user),
            "auth":str(request.auth)
        }


        return Response(data=content,status=status.HTTP_200_OK)