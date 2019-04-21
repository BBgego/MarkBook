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
    # 用户性别
    sex = models.CharField(max_length=10, default="男")
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
    # 登录验证
    token = models.CharField(max_length=200, unique=True, null=True)


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
    # 喜欢数
    love = models.IntegerField(default=0)
    # 浏览数
    look = models.IntegerField(default=0)
    # 是否删除
    is_del = models.BooleanField(default=False)


# 父级评论
class FatherArt(models.Model):
    # 评论内容
    content = models.CharField(max_length=200)
    # 评论用户
    user = models.ForeignKey(User, on_delete="PROTECT")
    # 评论文章
    book = models.ForeignKey(Book, on_delete="PROTECT")
    # 评论时间
    art_time = models.CharField(max_length=20)
    # 是否删除
    is_del = models.BooleanField(default=False)


# 子级评论
class SonArt(models.Model):
    # 评论内容
    content = models.CharField(max_length=200)
    # 评论用户
    user = models.ForeignKey(User, on_delete='PROTECT')
    # 回复用户
    send_user_name = models.CharField(max_length=50)
    # 评论时间
    art_time = models.CharField(max_length=20)
    # 是否删除
    is_del = models.BooleanField(default=False)


# 收藏的文章
class CollectionBook(models.Model):
    user = models.ForeignKey(User, on_delete='PROTECT')
    book = models.ForeignKey(Book, on_delete='PROTECT')
    create_time = models.CharField(max_length=20)
    is_del = models.BooleanField(default=False)


# 喜欢的文章
class LikeBook(models.Model):
    user = models.ForeignKey(User, on_delete='PROTECT')
    book = models.ForeignKey(Book, on_delete='PROTECT')
    create_time = models.CharField(max_length=20)
    is_del = models.BooleanField(default=False)


# 关注
class Focus(models.Model):
    user = models.ForeignKey(User, on_delete='PROTECT')
    be_focus_user = models.IntegerField()
    create_time = models.CharField(max_length=20)
    is_del = models.BooleanField(default=False)


# 轮播图
class Banner(models.Model):
    href = models.CharField(max_length=200, default="#")
    img = models.CharField(max_length=100)
    create_time = models.CharField(max_length=20)
    is_del = models.BooleanField(default=False)


