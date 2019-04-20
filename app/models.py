from django.db import models


# Create your models here.

# 用户表
class User(models.Model):
    # 用户sid
    sid = models.CharField(max_length=20, unique=True)
    # 用户名
    name = models.CharField(max_length=50)
    # 头像
    photo = models.CharField(max_length=100, default="default.jpg")
    # 用户性别  0：女 1：男
    sex = models.IntegerField(default=1)
    # 手机号
    tel = models.CharField(max_length=20, unique=True)
    # 邮箱
    email = models.CharField(max_length=20, unique=True, null=True)
    # 密码
    password = models.CharField(max_length=100)
    # 创建时间
    create_time = models.CharField(max_length=100)
    # 是否删除
    is_del = models.BooleanField(default=False)


# 文集
class Corpus(models.Model):
    # 文集名
    name = models.CharField(max_length=50)
    # 文件夹
    dir_name = models.CharField(max_length=50)
    # 用户关联
    user = models.ForeignKey(User, on_delete="PROTECT")
    # 创建时间
    create_time = models.CharField(max_length=50)
    # 是否删除
    is_del = models.BooleanField(default=False)


# 文章
class Book(models.Model):
    # 文章名
    name = models.CharField(max_length=50)
    # 文件
    file_name = models.CharField(max_length=50)
    # 文集关联
    corpus = models.ForeignKey(Corpus, on_delete="PROTECT")
    # 创建时间
    create_time = models.CharField(max_length=50)
    # 是否删除
    is_del = models.BooleanField(default=False)
