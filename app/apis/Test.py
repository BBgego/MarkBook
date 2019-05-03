from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from MarkBook.settings import EMAIL_HOST_USER


class TestAPI(APIView):
    def get(self, request):
        msg = "<b>测试文档</b>"
        res = send_mail("标题", "内容", EMAIL_HOST_USER, ["17720835750@163.com"], html_message=msg)
        print(res)
        return Response("success", status=status.HTTP_200_OK)
