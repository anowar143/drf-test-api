from django.contrib.auth.models import User
from rest_framework import serializers
from testapps.models import App


class AppUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "email", "date_joined")


class AppSerializer(serializers.ModelSerializer):
    user = AppUserSerializer(read_only=True)

    class Meta:
        model = App
        fields = ("user", "name", "done", "date_created")
