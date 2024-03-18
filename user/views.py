from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import UserModel
from user.serializers import UserSerializer


class CreateUserView(CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class ManageUserView(RetrieveUpdateAPIView):
    queryset = UserModel.objects.all()
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
