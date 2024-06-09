from django.shortcuts import render
from django.contrib.auth.hashers import make_password
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny

from user.pagination import pagination
from user.serializers import UserSerializer
from user.models import Friends, User
from user.utils import is_valid_email,auth_users,auth_token
from django.db.models import Q
from user.enum import EnumStatus
from datetime import datetime,timedelta, timezone

import logging
logger = logging.getLogger( __name__ )


class SignUP(APIView):
    def post(self,request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            email= data['email']
            password= data['password']
            confirm_password= data['confirm_password']

            if len(email)==0:
                return Response(data={"message":"Please enter email address"},status=status.HTTP_400_BAD_REQUEST)
            
            if User.objects.filter(email=email).exists():
                return Response(data={"message":"This email address is already exists, Please try another one"},status=status.HTTP_400_BAD_REQUEST)
             
            valid_email = is_valid_email(email)
            if valid_email==False:
                return Response(data={"message":"Please enter valid email address"},status=status.HTTP_400_BAD_REQUEST)

            if len(password)==0: 
                return Response(data={"message":"Please enter password"},status=status.HTTP_400_BAD_REQUEST)
            
            if len(confirm_password)==0: 
                return Response(data={"message":"Please enter confirm password"},status=status.HTTP_400_BAD_REQUEST)

            if password!=confirm_password:
                return Response(data={"message":"Please enter password and confirm password as same"},status=status.HTTP_400_BAD_REQUEST)
            
            #user create
            user= User.objects.create(name=data['name'],email=email,password=make_password(password))       
            token= auth_token(user)
            return Response(data={"message":"User created successfully",
                                  "access_token":token['access_token'],
                                  "refresh_token":token['refresh_token']},status=status.HTTP_200_OK)
                
        except Exception as e:
            logger.info(str(e),exc_info=True)


class Login(APIView):
    def post(self,request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            if not User.objects.filter(email=data['email']).exists():
                return Response(data="This email address does not exists",status=status.HTTP_400_BAD_REQUEST)
            
            user_password = auth_users(data['email'], data['password'])
            if user_password==False:
                return Response(data={"message":"Please enter correct password"},status=status.HTTP_400_BAD_REQUEST)
            
            user= User.objects.get(email=data['email'])
            token= auth_token(user)
            return Response(data={"message":"Logged in sucessfully",
                                  "access_token":token['access_token'],
                                  "refresh_token":token['refresh_token']},status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.info(str(e),exc_info=True)


class SearchUsers(APIView):
    permission_classes= [IsAuthenticated]

    def get(self,request):
        try:
            user= request.user.id
            #key validation
            if "search" in request.query_params:
                search = request.query_params.get('search')
            else:
                return Response(data={"message":"search keyword missing"},status=status.HTTP_400_BAD_REQUEST)

            if len(search)==0:
                return Response(data={"message":"search key is empty"},status=status.HTTP_400_BAD_REQUEST)

            email_match_queryset= User.objects.filter(email__exact=search).exclude(id=user)
            name_match_queryset= User.objects.filter(name__icontains=search).exclude(id=user)
            
            if email_match_queryset.exists():
                queryset= email_match_queryset
            else:
                queryset= name_match_queryset

            result= pagination(queryset,request,UserSerializer)
            return Response(data={"message":"firends list listed successfully","data":result},status=status.HTTP_200_OK)

        except Exception as e:
            logger.info(str(e),exc_info=True)


class FriendRequest(APIView):
    permission_classes= [IsAuthenticated]

    def post(self,request):
        """
        Making new friend request
        """
        try:
            data= json.loads(request.body.decode('utf-8'))
            firend_id= data['friend_requested_to']
            utc_time = datetime.now(timezone.utc)
            friend_count= Friends.objects.filter(requested_by_id=request.user.id,created_on__range=[utc_time-timedelta(minutes=1),utc_time]).count()
            if friend_count>=3:
                return Response(data={"message":"You can not send more than 3 friend requests within a minute."},status=status.HTTP_400_BAD_REQUEST) 


            if Friends.objects.filter(Q(requested_by_id=request.user.id,requested_to_id=firend_id)| Q(requested_by_id=firend_id,requested_to_id=request.user.id)).exists():
                return Response(data={"message":"Already this user in friend list"},status=status.HTTP_400_BAD_REQUEST)

            Friends.objects.create(requested_to_id=firend_id,requested_by_id=request.user.id,status=EnumStatus.pending.value)
            return Response(data={"message":"Friend request sent successfully"},status=status.HTTP_200_OK)

        except Exception as e:
            logger.info(str(e),exc_info=True)

    def get(self,request):
        """
        Pending firend requests list
        """
        try:
            pending_friends_id= Friends.objects.filter(requested_to_id=request.user.id,status=EnumStatus.pending.value).values_list('requested_by_id',flat=True)
            pending_friends= User.objects.filter(id__in=pending_friends_id)
            result= pagination(pending_friends,request,UserSerializer)
            return Response(data={"message":"Pending friends listed successfully","data":result},status=status.HTTP_200_OK)
        except Exception as e:
            logger.info(str(e),exc_info=True)

    def put(self,request):
        """
        Accept or reject friend request
        """
        try:
            data= json.loads(request.body.decode('utf-8'))
            firend_id= data['friend_requested_by']
            status_key= data['status']           

            if status_key=="accepted":
                key= "Friend request accepted successfully"

            elif status_key=="rejected":
                key="Friend request rejected successfully"

            else:
                key="invalid"
                
            #cheking that this user already in friendslist or not
            if Friends.objects.filter(Q(requested_by_id=request.user.id,requested_to_id=firend_id)| Q(requested_by_id=firend_id,requested_to_id=request.user.id),status=EnumStatus.accepted.value).exists():
                return Response(data={"message":"Already this user in friend list"},status=status.HTTP_400_BAD_REQUEST)
            
            Friends.objects.filter(requested_by_id=firend_id,requested_to_id=request.user.id,status=EnumStatus.pending.value).update(status=status_key,updated_on=datetime.now())
            return Response(data={"message":key},status=status.HTTP_200_OK)

        except Exception as e:
            print(str(e))
            logger.info(str(e),exc_info=True)


class AcceptedFriendsList(APIView):
    permission_classes= [IsAuthenticated]

    def get(self,request):
        try:
            user= request.user.id
            firends_queryset1= Friends.objects.filter(requested_by_id=request.user.id,status=EnumStatus.accepted.value).values_list('requested_to_id',flat=True)
            firends_queryset2= Friends.objects.filter(requested_to_id=request.user.id,status=EnumStatus.accepted.value).values_list('requested_by_id',flat=True)
            
            queryset = firends_queryset1.union(firends_queryset2)
            queryset= User.objects.filter(id__in=queryset)           
            result= pagination(queryset,request,UserSerializer)
            return Response(data={"message":"firends list listed successfully","data":result},status=status.HTTP_200_OK)

        except Exception as e:
            logger.info(str(e),exc_info=True)


