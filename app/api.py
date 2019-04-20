from django.http import JsonResponse
from django.views import View


class TestAPI(View):
    def get(self, request):
        return JsonResponse({
            "status": "200",
            "msg": "测试接口，访问成功!!"
        })
