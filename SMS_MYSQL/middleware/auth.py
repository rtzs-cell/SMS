from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class AuthMiddleware(MiddlewareMixin):
    """中间件1"""


    def process_request(self, request):
        # 排除不需要登录能访问的页面
        if request.path_info in ["/login/", "/image/code/"]:
            return

        info_dict = request.session.get("info")
        # 已登录
        if info_dict:
            return

        return redirect("/login/")



