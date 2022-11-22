from django.shortcuts import render, redirect
from django.views import View

from django.contrib import messages

from .forms import TrelloUserCreationForm
from .tokens import activateEmail


# Create your views here.

class DashboardView(View):
    def get(self, request):
        return render(request, "dashboard.html")


class RegisterView(View):

    # @user_not_authenticated
    def get(self, request):
        return render(request, "registration/register.html", {"form": TrelloUserCreationForm})

    # @user_not_authenticated
    def post(self, request):
        form = TrelloUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.backend = "django.contrib.auth.backends.ModelBackend"
            user.save()
            activateEmail(request, user, form.cleaned_data.get("email"))
            # login(request, user)
            return redirect("dashboard")
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
