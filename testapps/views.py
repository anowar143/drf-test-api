from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from testapps.models import App
from testapps.permissions import UserIsOwnerApp
from testapps.serializers import AppSerializer


class AppListCreateAPIView(ListCreateAPIView):
    serializer_class = AppSerializer

    def get_queryset(self):
        return App.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AppDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = (IsAuthenticated, UserIsOwnerApp)


