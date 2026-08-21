from django.contrib.auth.decorators import login_required
from django.http import request, response
from django.shortcuts import render
from architecture_ai.models import UserArchitecture

@login_required
def home(request):
    arc = UserArchitecture.objects.filter(user=request.user)
    context = {
        'arcs':arc
    }
    return render(request, 'main/index.html',context)