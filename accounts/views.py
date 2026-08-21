from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    context = {}
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        context["error"] = "Invalid email or password."
    return render(request, "accounts/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("login")

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Activity

from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.shortcuts import render
from .models import Activity


@login_required
def profile(request):
    today = date.today()
    start_date = today - timedelta(days=364)

    # Efficiently group and count in the database
    activities = (
        Activity.objects.filter(
            user=request.user, created_at__date__gte=start_date
        )
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(count=Count("id"))
    )

    # Format keys as "YYYY-MM-DD" strings
    activity_data = {
        item["day"].strftime("%Y-%m-%d"): item["count"]
        for item in activities
        if item["day"] is not None
    }

    return render(
        request,
        "accounts/profile/user_profile.html",
        {
            "user": request.user,
            "profile": getattr(request.user, "profile", None),
            "activity_data": activity_data,  # Matches {{ activity_data|json_script:"activity-data" }}
        },
    )
    
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileForm, UserUpdateForm


@login_required
def edit_profile(request):
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST,instance=request.user)
        profile_form = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("profile")
    return render(request,"accounts/profile/edit_profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        }
    )