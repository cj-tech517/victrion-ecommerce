from django.contrib import admin
from .models import Category, Product

# -------------------------
# CATEGORY ADMIN
# -------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)

# -------------------------
# PRODUCT ADMIN
# -------------------------
# Unregister first in case it was already registered
try:
    admin.site.unregister(Product)
except admin.sites.NotRegistered:
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    # 🔥 Allow selecting multiple related products to show as featured below this product
    filter_horizontal = ('related_products',)
