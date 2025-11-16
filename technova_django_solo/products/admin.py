from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, Review, Offer


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ['image', 'alt_text', 'sort_order']
    ordering = ['sort_order']

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
    list_display = ('name', 'category', 'brand', 'price', 'compare_at_price', 'stock_quantity', 'status', 'is_on_sale')
    list_filter = ('status', 'condition', 'category', 'brand', 'created_at')
    search_fields = ('name', 'description', 'brand')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-created_at',)
    inlines = [ProductImageInline]
    readonly_fields = ('created_at', 'updated_at', 'discount_percentage')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'slug', 'category', 'brand', 'model', 'sku')
        }),
        ('Descripción', {
            'fields': ('description', 'short_description')
        }),
        ('Precios', {
            'fields': ('price', 'compare_at_price', 'cost_price', 'discount_percentage'),
            'description': 'Establece un precio de comparación mayor al precio regular para activar la oferta'
        }),
        ('Inventario', {
            'fields': ('stock_quantity', 'low_stock_threshold', 'status', 'condition')
        }),
        ('Imágenes', {
            'fields': ('primary_image',),
            'description': 'La imagen principal del producto. Las imágenes adicionales se pueden agregar abajo'
        }),
        ('Especificaciones', {
            'fields': ('specifications', 'features', 'weight', 'dimensions')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        })
    )
    
    def is_on_sale(self, obj):
        if obj.compare_at_price and obj.compare_at_price > obj.price:
            return format_html(
                '<span style="color: green;">✓ En oferta (-{}%)</span>',
                obj.discount_percentage
            )
        return format_html('<span style="color: gray;">Regular</span>')
    is_on_sale.short_description = 'En oferta'
    
    def discount_percentage(self, obj):
        if obj.compare_at_price and obj.compare_at_price > obj.price:
            return f"{obj.discount_percentage}%"
        return "0%"
    discount_percentage.short_description = 'Descuento'

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'sort_order', 'image_preview')
    list_filter = ('product__category',)
    search_fields = ('product__name', 'alt_text')
    ordering = ('sort_order',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover;" />',
                obj.image.url
            )
        return "Sin imagen"
    image_preview.short_description = 'Vista previa'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'is_approved', 'is_verified_purchase', 'created_at')
    list_filter = ('rating', 'is_approved', 'is_verified_purchase', 'created_at')
    search_fields = ('product__name', 'user__username', 'title', 'comment')
    ordering = ('-created_at',)
    list_editable = ('is_approved', 'is_verified_purchase')
    
    fieldsets = (
        ('Información', {
            'fields': ('product', 'user', 'rating', 'title', 'comment')
        }),
        ('Estado', {
            'fields': ('is_approved', 'is_verified_purchase')
        }),
    )


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'discount_percentage', 'start_date', 'end_date', 'is_active', 'image_preview')
    list_filter = ('is_active', 'start_date')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Información de la Oferta', {
            'fields': ('title', 'description', 'image'),
            'description': 'Añade una imagen atractiva para la oferta'
        }),
        ('Precios', {
            'fields': ('price', 'discount_percentage', 'final_price'),
            'description': 'Configura el precio original y el descuento'
        }),
        ('Vigencia', {
            'fields': ('start_date', 'end_date', 'is_active'),
            'description': 'Establece el período de vigencia de la oferta'
        }),
    )
    
    readonly_fields = ('created_at', 'image_preview', 'final_price')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 150px; height: 150px; object-fit: cover; border-radius: 8px;" />',
                obj.image.url
            )
        return "Sin imagen"
    image_preview.short_description = 'Vista previa de la imagen'
    
    def final_price(self, obj):
        if obj.price and obj.discount_percentage:
            discount = obj.price * (obj.discount_percentage / 100)
            final_price = obj.price - discount
            return f"${final_price:.2f}"
        return obj.price or "Sin precio"
    final_price.short_description = 'Precio con descuento'
    
    class Media:
        css = {
            'all': ('admin/css/offers.css',)
        }
