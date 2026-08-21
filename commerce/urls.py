from django.urls import path
from . import views
urlpatterns = [
    path('',views.main, name="commerce-main"),
    path('details/<int:id>', views.product_detail, name="product-details")
]
