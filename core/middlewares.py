from django.utils.timezone import now

from core.models import MyUser


class LastActivityTraceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        member: MyUser = request.user
        if member.is_authenticated:
            member.last_request = now()
            member.save()
        return response
