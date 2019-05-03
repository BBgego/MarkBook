from django.urls import path

from app.apis.Test import TestAPI
from app.apis.User import UserAPI, VerifyCodeAPI, EmailVerifyAPI, ReEmailVerifyAPI, LoginAPI

urlpatterns = [
    path(r'test/', TestAPI.as_view()),  # 测试接口
    # 用户模块
    path(r'user/', UserAPI.as_view()),  # 用户
    path(r'verify_code/', VerifyCodeAPI.as_view()),  # 图形验证码
    path(r'email_verify/', EmailVerifyAPI.as_view()),  # 邮箱验证
    path(r're_email_verify/', ReEmailVerifyAPI.as_view()),  # 重新发送邮箱验证
    path(r'login/', LoginAPI.as_view())  # 登录


]
