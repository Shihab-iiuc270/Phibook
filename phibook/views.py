from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse, HttpResponseBadRequest


def api_root(request):
    return redirect('api-root')


def activate_account(request, uid, token):
    if request.method != "GET":
        return HttpResponseBadRequest("Invalid request method.")

    try:
        user_id = urlsafe_base64_decode(uid).decode()
        user = get_user_model().objects.get(pk=user_id)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        return HttpResponseBadRequest("Invalid activation link.")

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save(update_fields=["is_active"])
        return HttpResponse("Your account has been activated successfully.")

    return HttpResponseBadRequest("Activation link is invalid or expired.")

