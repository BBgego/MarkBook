from django.urls import path

from app.api import TestAPI

urlpatterns = [
    # 测试接口
    path(r'test/', TestAPI.as_view(), name="test"),

]
