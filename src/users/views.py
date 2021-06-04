from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate, login

UserModel = get_user_model()


class CustomSignupForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ("email",)


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")

            user = authenticate(email=email, password=raw_password)
            login(request, user)

            context = {}
            return render(request, "index", context)

    else:
        form = UserCreationForm()

    context = {"form": form, "errors": form.errors.values()}
    return render(request, "users/signup.html", context)
