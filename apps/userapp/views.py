from rest_framework import generics, permissions, views, response, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, UserSerializer, ChangePasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(generics.CreateAPIView):
    """POST /api/users/register/"""
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # User yaratamiz
        user = serializer.save()

        # JWT token generatsiya qilamiz
        refresh = RefreshToken.for_user(user)

        data = {
            "user": UserSerializer(user).data,  # yoki serializer.data ham bo‘lishi mumkin
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
    
class MeView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/users/me/"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class ChangePasswordView(views.APIView):
    """POST /api/users/change-password/"""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        ser = ChangePasswordSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        ser.save()
        return response.Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)