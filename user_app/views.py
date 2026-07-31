from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .serializers import (
    UserSerializer,
    LoginSerializer,
    LogoutSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@extend_schema(
    summary="Register a new user",
    description="Create a new user account and return JWT authentication tokens.",
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(description="User registered successfully"),
        400: OpenApiResponse(description="Validation error"),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        user_data = UserSerializer(user).data
        return Response({
            'message': 'Registration successful',
            'tokens': tokens,
            'user': user_data,
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="User Login",
    description="Authenticate user with username/email and password, returning JWT access and refresh tokens.",
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(description="Login successful"),
        400: OpenApiResponse(description="Missing credentials"),
        401: OpenApiResponse(description="Invalid credentials"),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    username_or_email = serializer.validated_data['username']
    password = serializer.validated_data['password']

    # Support login with email or username
    user = authenticate(username=username_or_email, password=password)
    if not user:
        try:
            user_obj = User.objects.get(email=username_or_email)
            user = authenticate(username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

    if user:
        if not user.is_active:
            return Response({'error': 'User account is disabled.'}, status=status.HTTP_400_BAD_REQUEST)

        tokens = get_tokens_for_user(user)
        user_data = UserSerializer(user).data
        return Response({
            'message': 'Login successful',
            'tokens': tokens,
            'user': user_data,
        }, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid username/email or password.'}, status=status.HTTP_401_UNAUTHORIZED)


@extend_schema(
    summary="User Logout",
    description="Blacklist the provided refresh token to logout user.",
    request=LogoutSerializer,
    responses={
        200: OpenApiResponse(description="Logged out successfully"),
        400: OpenApiResponse(description="Token error"),
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    serializer = LogoutSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh_token = serializer.validated_data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Change User Password",
    description="Change password for the currently logged in user.",
    request=ChangePasswordSerializer,
    responses={
        200: OpenApiResponse(description="Password changed successfully"),
        400: OpenApiResponse(description="Validation error"),
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'old_password': ['Incorrect old password.']}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    methods=['GET'],
    summary="Get Current User Profile",
    description="Retrieve details of currently authenticated user.",
    responses={200: UserSerializer}
)
@extend_schema(
    methods=['PUT', 'PATCH'],
    summary="Update Current User Profile",
    description="Update email, first_name, and last_name of currently authenticated user.",
    request=UserSerializer,
    responses={200: UserSerializer, 400: OpenApiResponse(description="Validation error")}
)
@api_view(['GET', 'PUT', 'PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method in ['PUT', 'PATCH']:
        partial = (request.method == 'PATCH')
        serializer = UserSerializer(request.user, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

