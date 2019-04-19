from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


# 测试视图
class TestView(View):
    def get(self, request):
        return HttpResponse("hello")
