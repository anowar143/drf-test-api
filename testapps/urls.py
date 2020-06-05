from django.urls import path
from testapps.views import AppListCreateAPIView, AppDetailAPIView

app_name = 'testapps'

urlpatterns = [
    path('', AppListCreateAPIView.as_view(), name="list"),
    path('<int:pk>/', AppDetailAPIView.as_view(), name="detail"),
]
