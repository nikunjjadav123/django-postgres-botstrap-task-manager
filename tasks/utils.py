from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from accounts.models import User


def get_logged_in_user(request):
    token = request.COOKIES.get("access_token")
    if not token:
        return None
    try:
        access_token = AccessToken(token)
        user_id = access_token["user_id"]
        return User.objects.get(id=user_id)
    except Exception:
        return None
