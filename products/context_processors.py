from django.db.models import Count
from .models import Category

def categories_processor(request):
    return {
        'sidebar_categories': Category.objects.annotate(
            product_count=Count('products')
        )
    }
