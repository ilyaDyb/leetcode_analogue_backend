from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.users.models import User
from core.users.serializaters import UserCreateSerializer
from .serializaters import MyTokenObtainPairSerializer


class CustomJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        token = super().get_validated_token(raw_token)
        jti = token['jti']
        if BlacklistedToken.objects.filter(token__jti=jti).exists():
            raise InvalidToken({"detail": "Token is blacklisted"})
        return token
    
class MyTokenObtaionPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class BaseAuthenticate:
    def __init__(self, headers: dict) -> None:
        self.token = headers.get("Authorization", None)
    
    @property
    def get_user_instance(self):
        if not self.token:
            raise AuthenticationFailed({"detail": "You cannot authenticate without authorization token"}, code=400)
        token_str = self.token.split()[1]
        token = AccessToken(token_str)
        user_id = token["user_id"]
        user_instance = User.objects.get(pk=user_id)
        return user_instance
    

class RegisterView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, example='string'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, example='email@example.com'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, example='string'),
            },
            required=['username', 'email', 'password']
        ),
        responses={201: UserCreateSerializer, 400: 'Bad Request'}
    )
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class LoginView(APIView):
    """Send username or email field"""
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, example='string'),
                # 'email': openapi.Schema(type=openapi.TYPE_STRING, example='email@example.com'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, example='string'),
            },
            required=['password']
        ),
        responses={201: UserCreateSerializer, 400: 'Bad Request'}
    )
    def post(self, request):
        email = request.data.get("email", None)
        username = request.data.get("username", None)
        password = request.data.get("password")

        if not (username or email) or not password:
            raise AuthenticationFailed(detail="Username or email and password are required", code=400)

        if username:
            user = User.objects.filter(username=username).first()
            field = "username"
        elif email:
            user = User.objects.filter(email=email).first()
            field = "email"
        else:
            raise AuthenticationFailed(detail="Unknown error", code=400)

        if user is None:
            raise AuthenticationFailed(detail=f"User with such {field} does not exist", code=400)

        if not user.check_password(password):
            raise AuthenticationFailed(detail="Incorrect password", code=400)

        refresh = RefreshToken.for_user(user=user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, example='string'),
            },
            required=['refresh']
        ),
        responses={205: "You have successfully logged out", 400: 'Bad Request'}
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "You have successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)