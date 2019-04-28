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
    sid = serializers.CharField(required=True)
    name = serializers.CharField(max_length=20, min_length=2, required=True)
    photo = serializers.CharField(max_length=100, default="default.jpg")
    sex = serializers.ChoiceField(choices=["男", "女"], required=True)
    email = serializers.CharField(max_length=20, required=True)
    password = serializers.CharField(required=True, max_length=200)
    create_time = serializers.CharField(required=True)
    token = serializers.CharField(max_length=200, required=True)

    def create(self, validated_data):
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
