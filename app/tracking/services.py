from tracking.models import UserAgentTracker


def track_user_agent(user, user_agent):
    UserAgentTracker.objects.update_or_create(
        user=user, defaults={"user_agent": user_agent}
    )
