from rest_framework.decorators import api_view
from django.contrib.gis.geos import Point
from rest_framework import generics
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


@api_view(['POST'])
def update_user_location(request):
    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')

    if not latitude or not longitude:
        return Response({"error": "Latitude and longitude are required."}, status=400)

    try:
        user = request.user
        user.location = Point(float(longitude), float(latitude), srid=4326)
        user.save()
        return Response({"message": "Location updated successfully."})
    except Exception as e:
        return Response({"error": str(e)}, status=500)
