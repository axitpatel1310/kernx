from architecture_ai.models import UserArchitecture
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from .models import Architecture, UserArchitecture, ArchitectureType,TechnologyCategory,Technology
from .llm import analyze_architecture
from accounts.models import Activity

def dataset_list(request):
    datasets = ArchitectureType.objects.order_by("name")
    return render(request,"architectures/all.html",
        {
            "datasets": datasets,
        },
    )


def dataset_detail(request, dataset):
    architecture_type = get_object_or_404(ArchitectureType,slug=dataset)
    architectures = (Architecture.objects.filter(type=architecture_type).order_by("title"))
    return render(request,"architectures/list.html",
        {
            "dataset": architectures,
            "main_type": architecture_type.name,
            "architecture_type": architecture_type,
        },
    )

def architecture_detail(request, dataset, id):
    architecture = get_object_or_404(Architecture,id=id,type__slug=dataset)
    return render(request,"architectures/detail.html",
        {
            "dataset": dataset,
            "architecture": architecture.data,
            "architecture_obj": architecture,
        },
    )
    
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import (Architecture,UserArchitecture,ProjectField,TechnologyCategory)

@login_required
def edit_architecture(request, dataset, id):
    original = get_object_or_404(Architecture,id=id,type__slug=dataset)
    user_architecture = UserArchitecture.objects.create(user=request.user,original=original,name=original.title,data=original.data)
    Activity.objects.create(user=request.user,activity_type="architecture_created")
    return redirect("user-architecture-detail",id=user_architecture.id)

from markdown import markdown
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import (UserArchitecture,ProjectField,TechnologyCategory)

@login_required
def user_architecture_detail(request, id):
    architecture = get_object_or_404(UserArchitecture,id=id,user=request.user)
    original = architecture.original
    project_fields = ProjectField.objects.all()
    technology_categories = (TechnologyCategory.objects.prefetch_related("technologies"))
    if request.method == "POST":
        data = architecture.data.copy()
        # Update project fields
        for field in project_fields:
            value = request.POST.get(f"project.{field.key}")
            if value is not None:
                data["project"][field.key] = value
        for category in technology_categories:
            value = request.POST.get(f"recommended_stack.{category.slug}")
            if value:
                data["recommended_stack"][category.slug] = value
        architecture.data = data
        architecture.name = data["project"]["name"]
        architecture.save()
        Activity.objects.create(user=request.user,activity_type="architecture_updated")
        return redirect("user-architecture-detail",id=architecture.id,)
    return render(request,"architectures/editor.html",
            {
            "reference": original,
            "architecture": architecture,
            "project_fields": project_fields,
            "technology_categories": technology_categories,
        },
    )
    
from django.http import JsonResponse
from markdown import markdown
from .llm import analyze_architecture
import time

@login_required
def analyze_user_architecture(request, id):
    architecture = get_object_or_404(UserArchitecture,id=id,user=request.user)
    start = time.time()
    analysis = markdown(analyze_architecture(architecture.data),extensions=["extra"])
    print(f"Ollama analysis took {time.time() - start:.2f}s")
    return render(request,"architectures/anaylsis.html",{"analysis": analysis})
    
def delete_architecture(request,id):
    architecture = get_object_or_404(UserArchitecture,id=id,user=request.user)
    architecture.delete()
    return redirect("home")