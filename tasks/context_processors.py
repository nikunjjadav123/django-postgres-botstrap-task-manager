from tasks.utils import get_logged_in_user

def logged_user(request):
    return {
        "logged_user": get_logged_in_user(request)
    }
