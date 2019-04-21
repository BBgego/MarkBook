from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class HeaderMiddleware(MiddlewareMixin):
    def process_request(self, request):
        headers = request.headers
        print(headers)
        # if headers.get("Accept") != "application/json":
        #     return JsonResponse({
        #         "status": "403",
        #         "msg": "拒绝访问"
        #     })
