import uuid
from django.contrib.auth.hashers import check_password
from django.core.cache import cache
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.extends.sms import SMS
from app.models import User
from app.serializers.UserSerializer import UserCreateSerializer


# 登录
class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        user = data.get("user")
        password = data.get("password")
        try:
            user = User.objects.get(Q(email=user) | Q(sid=user))
            if check_password(password, user.password):
                if user.is_del:
                    return Response("账号已被禁用", status=status.HTTP_403_FORBIDDEN)
                if not user.is_verify:
                    return Response("账号未激活", status=status.HTTP_404_NOT_FOUND)
                token = str(uuid.uuid1())
                user.token = token
                return Response({
                    "msg": "验证成功",
                    "token": token
                }, status=status.HTTP_200_OK)
            else:
                return Response("密码错误", status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            print(ex)
            return Response("用户信息错误", status=status.HTTP_402_PAYMENT_REQUIRED)


# 用户
class UserAPI(APIView):
    def post(self, request):
        token = str(uuid.uuid1())
        request.data["token"] = str(uuid.uuid1())
        serializer = UserCreateSerializer(data=request.data, many=False)
        if serializer.is_valid():
            # 判断邮箱或用户名是否存在
            user = User.objects.filter(name=request.data["name"])
            if user:
                return Response("用户名已存在", status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.filter(email=request.data["email"])
            if user:
                return Response("邮箱已注册", status=status.HTTP_401_UNAUTHORIZED)
            sms = SMS(request.data["email"], token)
            if sms.send():
                serializer.save()
                cache.set(request.data["email"], {
                    "token": token,
                    "sign": "1"
                }, 60*5)
                return Response("发送验证邮件成功,请在5分钟之内完成验证", status=status.HTTP_200_OK)
            else:
                return Response("该邮箱无法接受邮件", status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class ReVerEmail(APIView):
    def post(self, request):
        email = request.data.get("email")
        if email:
            sms = SMS(email, token=str(uuid.uuid1()))
            if sms.send():
                return Response("重新发送邮件成功", status=status.HTTP_200_OK)
            return Response("发送邮件失败，邮箱不支持", status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response("参数错误", status=status.HTTP_403_FORBIDDEN)

