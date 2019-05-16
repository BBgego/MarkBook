from django.urls import path

from app.apis.Test import TestAPI
from app.apis.User import UserAPI, LoginAPI, ReVerEmail

urlpatterns = [
    path(r'test/', TestAPI.as_view()),  # 测试接口
    path(r'login/', LoginAPI.as_view()),  # 登录
    path(r're_ver_email/', ReVerEmail.as_view()),   # 重新发送邮件
    # 用户模块
    path(r'user/', UserAPI.as_view()),  # 用户





]
