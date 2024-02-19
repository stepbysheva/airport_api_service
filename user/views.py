from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView

from user.models import UserModel
from user.serializers import UserSerializer


class CreateUserView(CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class ManageUserView(RetrieveUpdateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
