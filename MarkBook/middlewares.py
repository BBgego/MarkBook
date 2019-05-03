from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status


class HeaderMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # headers = request.headers
        # if headers.get("Content-Type") != "application/json" and headers.get("User-Agent"):
        #     res = JsonResponse({"msg": "Error"})
        #     res.status_code = 403
        #     return res
        pass
