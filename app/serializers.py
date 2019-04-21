from rest_framework import serializers

from app.models import Banner, User, Corpus


# 用户
class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    sid = serializers.IntegerField(required=True)
    name = serializers.CharField(max_length=50, required=True)
    photo = serializers.CharField(max_length=100, default="default.jpg")
    sex = serializers.ChoiceField(choices=["男", "女"], default="男")
    tel = serializers.CharField(max_length=20, required=True)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(max_length=100, required=True, min_length=6)
    create_time = serializers.CharField(read_only=True)
    is_del = serializers.BooleanField(read_only=True, default=False)
    token = serializers.CharField(max_length=200, allow_null=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.sex = validated_data.get('sex', instance.sex)
        instance.tel = validated_data.get('tel', instance.tel)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.token = validated_data.get('token', instance.token)
        instance.save()
        return instance


# 文集
class CorpusSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50, required=True)

    class Meta:
        model = Corpus
        fields = ('id', 'name')

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


# 轮播图
class BannerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50, required=True)
    love = serializers.IntegerField()

    class Meta:
        model = Banner
        fields = ('id', 'href', 'img')
