from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.db.models import Q
from .models import Product, Order
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post']  # Allow both GET and POST

def product_list(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def order_create(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        Order.objects.create(user=request.user, product=product, quantity=quantity)
        return redirect('product_list')
    return render(request, 'store/order_form.html', {'product': product})

@staff_member_required
def admin_dashboard(request):
    orders = Order.objects.all()
    # Aggregate orders by product category (year)
    order_data = Order.objects.values('product__category__name').annotate(count=Count('id'))
    years = [item['product__category__name'] for item in order_data]
    counts = [item['count'] for item in order_data]
    return render(request, 'store/admin_dashboard.html', {
        'orders': orders,
        'years': years,
        'counts': counts
    })