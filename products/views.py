from django.shortcuts import render
from django.shortcuts import render
from .models import Product
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category
from django.db.models import Count







# -----------------------------
# HOME PAGE VIEW
# -----------------------------
def home(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')

    products = Product.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    # Categories for sidebar with counts
    categories = Category.objects.annotate(product_count=Count('products'))

    return render(request, 'home.html', {
        'products': products,
        'sidebar_categories': categories,
        'query': query,
        'selected_category': category_id,
        'active_category': None,  # No active category on home
    })


# -----------------------------
# CATEGORY PAGE VIEW
# -----------------------------
def category_products(request, slug):
    category = get_object_or_404(
        Category.objects.annotate(product_count=Count('products')),
        slug=slug
    )

    query = request.GET.get('q', '')
    products = Product.objects.filter(category=category)

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    return render(request, 'category_products.html', {
        'category': category,
        'products': products,
        'sidebar_categories': Category.objects.annotate(product_count=Count('products')),
        'query': query,
        'active_category': category.slug,
    })


# -----------------------------
# PRODUCT DETAIL PAGE VIEW
# -----------------------------
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    return render(request, 'product_detail.html', {
        'product': product,
        'category': product.category,
        'sidebar_categories': Category.objects.annotate(product_count=Count('products')),
        'active_category': product.category.slug,
    })
