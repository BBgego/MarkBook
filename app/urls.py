from django.urls import path

from app.apis.User import UserAPI, VerifyCodeAPI

urlpatterns = [
    path(r'user/', UserAPI.as_view()),
    path(r'verify_code/', VerifyCodeAPI.as_view())  # 图形验证码
]
