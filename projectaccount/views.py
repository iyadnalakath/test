from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import LoginSerializer, RegisterCustomerSerializer,RegisterEventTeamSerializer,UserListSerializer,EventManagementListSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.core.exceptions import PermissionDenied
from rest_framework import generics
from .models import *
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.viewsets import ModelViewSet


# Create your views here.

# class LoginView(APIView):
    # def post(self, request):
    #     serializer = LoginSerializer(data=request.data)
    #     if serializer.is_valid():
    #         user = serializer.validated_data
    #         return Response(status=status.HTTP_200_OK)
    #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 

#     context = {}
#     username = request.data.get('username')
#     password = request.data.get('password')
#     account = authenticate(username=username, password=password )

#     if account:
#         try:
#             token = Token.objects.get(user=account)
#         except Token.DoesNotExist:
#             token = Token.objects.create(user=account)
#         context['response'] = 'Successfully authenticated.'
#         context['pk'] = account.pk
#         context['username'] = username.lower()
#         context['token'] = token.key
#         context['role'] = account.role
#         return Response(context,status=status.HTTP_200_OK)
#     else:
#         context['response'] = 'Error'
#         context['error_message'] = 'The username or password is incorrect'
#         return Response(context,status=status.HTTP_401_UNAUTHORIZED)


        

# class RegisterView(APIView):
#     permission_classes= [AllowAny]
#     def post(self,request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             account = serializer.save()

#             data['email'] = account.email
#             data['username'] = account.username
#             data['pk'] = account.pk
#             data['response'] = 'successfully registered new user.'

#             token = Token.objects.get(user=account).key
#             data['token'] = token
            
#             status_code=status.HTTP_200_OK
#             return Response(data,status=status_code)
#         else:
#             data = serializer.errors
#         return Response(data,status=status.HTTP_401_UNAUTHORIZED)
        

class RegisterCustomerView(APIView):
    permission_classes= [AllowAny]
    def post(self,request):
        serializer = RegisterCustomerSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()

            data['email'] = account.email
            data['username'] = account.username
            data['pk'] = account.pk
            data['response'] = 'successfully registered new user.'

            token = Token.objects.get(user=account).key
            data['token'] = token
            
            status_code=status.HTTP_200_OK
            return Response(data,status=status_code)
        else:
            data = serializer.errors
        return Response(data,status=status.HTTP_401_UNAUTHORIZED)
    

class RegisterEventTeamView(APIView):
    permission_classes= [AllowAny]
    def post(self,request):
        serializer =RegisterEventTeamSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()

            data['email'] = account.email
            data['username'] = account.username
            data['pk'] = account.pk
            data['response'] = 'successfully registered new user.'

            token = Token.objects.get(user=account).key
            data['token'] = token
            
            status_code=status.HTTP_200_OK
            return Response(data,status=status_code)
        else:
            # data = serializer.errors
            return Response(serializer.errors,status=status.HTTP_401_UNAUTHORIZED)
        

    

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset().order_by('auto_id')
        if self.request.user.role == 'admin' :
            serializer=RegisterEventTeamSerializer(queryset,many=True)
            # return super().list(request, *args, **kwargs)
            return Response (serializer.data,status=status.HTTP_200_OK)

        else:
            raise PermissionDenied("You are not allowed to retrieve this object.")








# class RegisterView(APIView):
#     def post(self,request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response(status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LoginView(APIView):
        
#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data
#         return Response(
#             {
#                 'user': LoginSerializer(
#                     user, context=self.get_serializer_context()
#                 ).data,
#                 'token': Token.objects.create(user)[1]
#             }
        # )
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        context = {}
        if serializer.is_valid():
            user = serializer.validated_data
            
            username = request.data.get('username')
            password = request.data.get('password')
            try:
                token= Token.objects.get(user=user)
            except:
                token= Token.objects.create(user=user)

            context['response'] = 'Successfully authenticated.'
            context['pk'] = user.pk
            context['username'] = username.lower()
            context['token'] = token.key
            context['role'] = user.role
            context['response'] = 'Successfully authenticated.'
            return Response(context,status=status.HTTP_200_OK)
        else:
            context['response'] = 'Error'
            context['error_message'] = 'The username or password is incorrect'
            return Response(context,status=status.HTTP_401_UNAUTHORIZED)

            # return Response(
            # {
            #     'user': serializer(
            #         user, context=self.get_serializer_context()
            #     ).data,
            #     'token': Token.objects.create(user)[1]
            # }
            # )
        

class ListUsersView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = UserListSerializer
    permission_classes=[IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        if self.request.user.role == 'admin':
            serializer=UserListSerializer(queryset,many=True)
            # return super().list(request, *args, **kwargs)
            return Response (serializer.data,status=status.HTTP_200_OK)

        else:
            raise PermissionDenied("You are not allowed to retrieve this object.")
        

class EventManagementUsersView(generics.ListAPIView):
    queryset = Account.objects.filter(role='event_management')
    serializer_class = EventManagementListSerializer

    
    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        if self.request.user.role == 'admin':
            serializer=EventManagementListSerializer(queryset,many=True)
            # return super().list(request, *args, **kwargs)
            return Response (serializer.data,status=status.HTTP_200_OK)

        else:
            raise PermissionDenied("You are not allowed to retrieve this object.")
