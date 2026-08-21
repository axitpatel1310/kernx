from django.urls import path
from . import views

urlpatterns = [
    path("", views.dataset_list, name="dataset-list"),
    path("<slug:dataset>/", views.dataset_detail, name="dataset-detail"),
    path("<slug:dataset>/<uuid:id>/",views.architecture_detail,name="architecture-detail"),
    
    path("<slug:dataset>/<uuid:id>/edit/",views.edit_architecture,name="architecture-edit"),
    path("my/<int:id>/",views.user_architecture_detail,name="user-architecture-detail"),
    path("my/<int:id>/analyze/",views.analyze_user_architecture,name="analyze-user-architecture"),
    path("my/<int:id>/delete",views.delete_architecture,name="architecture-delete")
]