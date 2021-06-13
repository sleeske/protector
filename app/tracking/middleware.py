from tracking.services import track_user_agent


class TrackUserAgentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user_agent = request.META["HTTP_USER_AGENT"]
            track_user_agent(request.user, user_agent)

        response = self.get_response(request)

        return response
