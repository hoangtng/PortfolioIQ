from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, UserDetailSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    # Allow anyone to register
    permission_classes = [permissions.AllowAny] 

class MeView(generics.RetrieveAPIView):
    # Allow users to view their own details
    # Must be loggin to access this endpoint
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)