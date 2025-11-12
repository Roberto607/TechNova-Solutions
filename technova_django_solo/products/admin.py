from django.contrib import admin
from .models import Category, Product, ProductImage, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'is_active', 'sort_order')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('sort_order', 'name')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'slug', 'parent', 'description')
        }),
        ('Configuración', {
            'fields': ('image', 'is_active', 'sort_order')
        }),
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price', 'stock_quantity', 'status')
    list_filter = ('status', 'condition', 'category')
    search_fields = ('name', 'description', 'brand')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'slug', 'category', 'brand', 'model')
        }),
        ('Descripción', {
            'fields': ('description', 'short_description')
        }),
        ('Precios', {
            'fields': ('price', 'compare_at_price', 'cost_price')
        }),
        ('Inventario', {
            'fields': ('stock_quantity', 'low_stock_threshold', 'status', 'condition')
        }),
        ('Imágenes', {
            'fields': ('primary_image',)
        }),
        ('Especificaciones', {
            'fields': ('specifications', 'features')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'sort_order')
    list_filter = ('product',)
    search_fields = ('product__name', 'alt_text')
    ordering = ('sort_order',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('product__name', 'user__username', 'title', 'comment')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Información', {
            'fields': ('product', 'user', 'rating', 'title', 'comment')
        }),
        ('Estado', {
            'fields': ('is_approved', 'is_verified_purchase')
        }),
    )
