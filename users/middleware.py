from django.utils import timezone


class BlueBadgeVerificationMiddleware:
    """
    Keeps `User.is_verified` in sync with `User.blue_badge_until`.
    When the badge expires, the flag is turned off on the next request.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        if user and getattr(user, "is_authenticated", False):
            blue_badge_until = getattr(user, "blue_badge_until", None)
            if user.is_verified and blue_badge_until and blue_badge_until <= timezone.now():
                user.is_verified = False
                user.blue_badge_until = None
                user.save(update_fields=["is_verified", "blue_badge_until"])

        return self.get_response(request)

