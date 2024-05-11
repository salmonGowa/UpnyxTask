from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status,generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User,Chat
from .serializers import UserSerializer,ChatSerializer


@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.tokens = 4000
        user.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    if user.password != password:
        return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
    
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key})

@api_view(['POST'])
def chat(request):
    token = request.data.get('token')
    message = request.data.get('message')
    
    try:
        user = Token.objects.get(key=token).user
    except Token.DoesNotExist:
        return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
    
    if user.tokens < 100:
        return Response({"error": "Insufficient tokens"}, status=status.HTTP_403_FORBIDDEN)
    
    # Deduct 100 tokens for each question asked
    user.tokens -= 100
    user.save()
    
    # Dummy response for each message (replace with AI-generated response)
    response = "Dummy AI response"
    
    # Save chat history
    Chat.objects.create(user=user, message=message, response=response)
    
    return Response({"response": response})

@api_view(['POST'])
def token_balance(request):
    token = request.data.get('token')
    
    try:
        user = Token.objects.get(key=token).user
    except Token.DoesNotExist:
        return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response({"tokens": user.tokens})
