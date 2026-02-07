from .models import Product
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category
from django.db.models import Count
from django.db.models import Q, Count




# def home(request):
#     query = request.GET.get('q', '')
#     category_id = request.GET.get('category')

#     products = Product.objects.all().order_by('-created_at')

#     if category_id:
#         products = products.filter(category_id=category_id)

#     if query:
#         products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

#     categories = Category.objects.annotate(product_count=Count('products'))

#     # 5 newest products for sidebar
#     newest_products = Product.objects.all().order_by('-created_at')[:5]

#     return render(request, 'home.html', {
#         'products': products,
#         'sidebar_categories': categories,
#         'newest_products': newest_products,
#         'query': query,
#         'selected_category': category_id,
#         'active_category': None,
#     })


# def category_products(request, slug):
#     category = get_object_or_404(
#         Category.objects.annotate(product_count=Count('products')),
#         slug=slug
#     )

#     query = request.GET.get('q', '')
#     products = Product.objects.filter(category=category).order_by('-created_at')

#     if query:
#         products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

#     categories = Category.objects.annotate(product_count=Count('products'))

#     # 5 newest products for sidebar
#     newest_products = Product.objects.all().order_by('-created_at')[:5]

#     return render(request, 'category_products.html', {
#         'category': category,
#         'products': products,
#         'sidebar_categories': categories,
#         'newest_products': newest_products,
#         'query': query,
#         'active_category': category.slug,
#     })



# # -----------------------------
# # PRODUCT DETAIL PAGE VIEW
# # -----------------------------
# def product_detail(request, slug):
#     product = get_object_or_404(Product, slug=slug)
#     # Get manually selected related products
#     related_products = product.related_products.all()
#      # Get featured/related products
#     featured = product.related_products.all()  # This will be empty if none selected

#     return render(request, 'product_detail.html', {
#         'product': product,
#         'category': product.category,
#         'featured_products': featured,
#         'related_products': related_products,
#         'sidebar_categories': Category.objects.annotate(product_count=Count('products')),
#         'active_category': product.category.slug,
#     })



# -----------------------------
# HOME PAGE VIEW
# -----------------------------
def home(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
       # Latest 5 products for sidebar / new arrivals
    latest_products = Product.objects.order_by('-created_at')[:5]

    products = Product.objects.all().order_by('-created_at')  # Newest first

    if category_id:
        products = products.filter(category_id=category_id)
        

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    categories = Category.objects.annotate(product_count=Count('products'))

    return render(request, 'home.html', {
        'products': products,
        'sidebar_categories': categories,
        'query': query,
         'latest_products': latest_products,  # Pass it to template
        'selected_category': category_id,
        'active_category': None,
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
    products = Product.objects.filter(category=category).order_by('-created_at')

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    categories = Category.objects.annotate(product_count=Count('products'))

    return render(request, 'category_products.html', {
        'category': category,
        'products': products,
        'sidebar_categories': categories,
        'query': query,
        'active_category': category.slug,
    })


# -----------------------------
# PRODUCT DETAIL PAGE VIEW
# -----------------------------
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    categories = Category.objects.annotate(product_count=Count('products'))

    # Latest 5 products
    latest_products = Product.objects.order_by('-created_at')[:5]

    # Featured / related products
    featured_products = product.related_products.all()

    return render(request, 'product_detail.html', {
        'product': product,
        'sidebar_categories': categories,
        'active_category': product.category.slug,
        'latest_products': latest_products,
        'featured_products': featured_products,
    })








