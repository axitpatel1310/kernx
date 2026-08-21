from django.shortcuts import render, get_object_or_404
from .models import digital_products


def main(request):
    products = digital_products.objects.all()
    return render(request,'commerce/main.html',{'products':products})

def product_detail(request, id):
    product = get_object_or_404(digital_products, id=id)
    context = {
        'product': product
    }
    return render(request,'commerce/detail.html', context)