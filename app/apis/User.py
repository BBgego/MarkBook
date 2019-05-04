import string
import time
import uuid
from random import randint, choice

from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.extends.random_code import get_random_code, md5_code
from app.extends.sms import SMS
from app.models import User
from app.serializers.UserSerializer import UserSerializer, UserCreateSerializer, UserUpdateSerializer


# 验证码
class VerifyCodeAPI(APIView):
    def get(self, request, format=None):
        token = request.GET.get("token")
        if token:
            code = get_random_code()
            m_code = md5_code(code)
            cache.set("ver=" + token, m_code, 60 * 3)
            return Response({"code": code}, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "参数错误"}, status=status.HTTP_400_BAD_REQUEST)


# 用户
class UserAPI(APIView):
    def get(self, request, format=None):
        print(request.data)
        id = request.GET.get("id")
        token = request.GET.get("token")
        try:
            user = User.objects.get(Q(id=int(id)), Q(token=token), Q(is_del=False))
            serializer = UserSerializer(user)

            return Response({
                "sid": serializer.data.get("sid"),
                "name": serializer.data.get("name"),
                "photo": serializer.data.get("photo"),
                "sex": serializer.data.get("sex"),
            }, status=status.HTTP_200_OK)

        except Exception as ex:
            print(ex)
            return Response({"msg": "信息错误"}, status=status.HTTP_401_UNAUTHORIZED)

    # 注册
    def post(self, request, format=None):
        data = request.data
        if (not data.get("code_token")) or (not data.get("ver_code")):
            return Response({
                "msg": "参数错误"
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if not cache.get("ver=" + data.get("code_token")):
            return Response({
                "msg": "图形验证码已过期"
            }, status=status.HTTP_403_FORBIDDEN)
        if cache.get("ver=" + data.get("code_token")) != data.get("ver_code"):
            return Response({
                "msg": "验证码错误"
            }, status=status.HTTP_404_NOT_FOUND)
        now_time = int(time.time())
        data["sid"] = str(choice(string.ascii_letters)) + str(now_time) + str(randint(1, 9))
        data["token"] = str(uuid.uuid1())
        if data.get("password"):
            data["password"] = make_password(data.get("password"), None, "pbkdf2_sha256")
        data["create_time"] = str(now_time)
        serializer = UserCreateSerializer(data=data)
        if serializer.is_valid():
            email = data.get("email")
            try:
                # 发送邮件并设置缓存
                sms = SMS(email, data.get("token"))
                if sms.send():
                    serializer.save()
                    cache.set(email, data.get("token"), 60 * 5)
                    return Response("success", status=status.HTTP_200_OK)
                else:
                    return Response("error", status=status.HTTP_406_NOT_ACCEPTABLE)
            except Exception as ex:
                print(ex)
                user = User.objects.filter(email=email)[0]
                if user.is_verify:
                    return Response({
                        "msg": "邮箱已注册"
                    }, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    # 发送邮件并设置缓存
                    sms = SMS(email, data.get("token"))
                    if sms.send():
                        user = User.objects.filter(email=email)[0]
                        data["id"] = user.id
                        serializer = UserUpdateSerializer(user, data=data)
                        if serializer.is_valid():
                            serializer.save()
                        cache.set(email, data.get("token"), 60 * 5)
                        return Response({
                            "msg": "邮箱已注册，但未验证，已重新发送邮件，请注意查收"
                        }, status=status.HTTP_402_PAYMENT_REQUIRED)
                    else:
                        return Response("success", status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        id = request.data.get("id")
        token = request.data.get("token")
        try:
            user = User.objects.get(Q(id=id), Q(token=token), Q(is_del=False))
            serializer = UserUpdateSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "msg": "修改成功"
                }, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            print(ex)
            return Response({"msg": "请先登录"}, status=status.HTTP_401_UNAUTHORIZED)


# 邮箱验证
class EmailVerifyAPI(APIView):
    def get(self, request):
        email = request.GET.get("email")
        token = request.GET.get("token")
        if (not email) or (not token):
            return Response("参数错误", status=status.HTTP_401_UNAUTHORIZED)
        c_token = cache.get(email)
        if not c_token:
            return Response("验证信息已过期", status=status.HTTP_402_PAYMENT_REQUIRED)
        if token == c_token:
            user = User.objects.filter(email=email)[0]
            if user.is_verify:
                return Response("邮箱已验证", status=status.HTTP_404_NOT_FOUND)
            token = str(uuid.uuid1())
            user.token = token
            user.is_verify = True

            user.save()
            return Response({
                "msg": "验证成功",
                "id": user.id,
                "token": token,
            }, status=status.HTTP_201_CREATED)
        return Response("验证错误", status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        data = request.data
        email = data.get("email")
        if not email:
            return Response("参数错误", status=status.HTTP_401_UNAUTHORIZED)
        user = User.objects.filter(email=email)
        try:
            user = user[0]
            if user.is_verify:
                user.token = str(uuid.uuid1())
                user.save()
                return Response({
                    "user": user.id,
                    "token": user.token
                }, status=status.HTTP_200_OK)
            else:
                return Response("", status=status.HTTP_201_CREATED)
        except Exception as ex:
            print(ex)
            return Response("用户不存在", status=status.HTTP_402_PAYMENT_REQUIRED)


class ReEmailVerifyAPI(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response("参数错误", status=status.HTTP_401_UNAUTHORIZED)
        user = User.objects.filter(email=email)
        try:
            user = user[0]
            user.token = str(uuid.uuid1())
            cache.set(email, user.token, 60 * 5)
            sms = SMS(email, user.token)
            sms.send()
            user.save()
            return Response({
                "id": user.id,
                "token": user.token
            }, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
            return Response("注册信息不存在", status=status.HTTP_402_PAYMENT_REQUIRED)


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
                return Response("验证成功", status=status.HTTP_200_OK)
            else:
                return Response("密码错误", status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            print(ex)
            return Response("用户信息错误", status=status.HTTP_402_PAYMENT_REQUIRED)
