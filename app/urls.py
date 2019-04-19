from django.urls import path

from app.views import TestView

urlpatterns = [
    # 测试视图
    path(r'test/', TestView.as_view(), name="test"),
]
