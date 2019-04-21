import time

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import User
from app.serializers import UserSerializer


class UserAPI(APIView):
    def get(self, request, format=None):
        id = request.GET.get("id")
        user = User.objects.filter(id=id)
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.POST.copy()
        print(data)
        data["sid"] = str(int(time.time()))
        data["token"] = "123456789"
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
