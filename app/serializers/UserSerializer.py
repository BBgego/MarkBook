import random
import string
import time
import uuid

from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from app.models import Banner, User, Corpus

'''
用户模块
'''


# 查询
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('create_time', 'token', 'is_del', 'password')


# 增加
class UserCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20, min_length=2, required=True, error_messages={
        "required": "请输入用户名",
        "min_length": "用户名长度必须>=2",
        "max_length": "用户名长度必须<=20"
    })
    email = serializers.CharField(max_length=20, required=True, error_messages={
        "required": "请输入邮箱",
        "max_length": "邮箱长度必须<=20"
    })
    password = serializers.CharField(required=True, min_length=6, max_length=20, error_messages={
        "required": "请输入密码",
        "min_length": "密码长度必须>=6",
        "max_length": "密码长度必须<=20"
    })
    token = serializers.CharField(max_length=100, required=True)

    def create(self, validated_data):
        # 生成账号
        validated_data["sid"] = random.choice(string.ascii_lowercase)
        validated_data["sid"] += random.choice(string.ascii_lowercase)
        validated_data["sid"] += random.choice(string.ascii_lowercase)
        validated_data["sid"] += str(random.randint(10000000, 1000000000))

        validated_data["password"] = make_password(validated_data["password"], None, "pbkdf2_sha256")
        validated_data["create_time"] = str(int(time.time()))
        return User.objects.create(**validated_data)


# 更新
class UserUpdateSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    name = serializers.CharField(max_length=20, min_length=2, required=True)
    photo = serializers.CharField(max_length=100, default="default.jpg")
    sex = serializers.ChoiceField(choices=["男", "女"], required=True)
    token = serializers.CharField(max_length=200, required=True)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.sex = validated_data.get('sex', instance.sex)
        instance.save()
        return instance
# # 文集
# class CorpusSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(max_length=50, required=True)
#
#     class Meta:
#         model = Corpus
#         fields = ('id', 'name')
#
#     def create(self, validated_data):
#         return User.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.save()
#         return instance
#
#
# # 轮播图
# class BannerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Banner
#         fields = ('id', 'href', 'img')
