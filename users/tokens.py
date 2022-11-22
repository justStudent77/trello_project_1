from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import login, get_user_model
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages

from .decorators import user_not_authenticated
import six


# ----------------------------------------------
# Token generation for account activation

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()


# ----------------------------------------------
# User activation
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thanks for your email confirmation. Now you can login your account")
        return redirect("login")
    else:
        messages.error(request, "Activation link is invalid")

    return redirect("home")


def activateEmail(request, user, to_email):
    mail_subject = "Follow this link to activate your account"
    message = render_to_string("registration/template_activate_account.html",
                               {"user": user.username,
                                "domain": get_current_site(request).domain,
                                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                                "token": account_activation_token.make_token(user),
                                "protocol": "https" if request.is_secure() else "http"})
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f"Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.")
    else:
        messages.error(request, f"Problem sending email to {to_email}, check if you typed it correctly")
