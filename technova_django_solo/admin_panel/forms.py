from django import forms
from products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductForm(forms.ModelForm):
    specifications_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 5}),
        label='Especificaciones',
        help_text='Introduce una especificación por línea en formato "clave: valor". Ej: "RAM: 8GB"'
    )

    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'short_description', 'description', 'category', 'brand', 'model',
            'sku', 'price', 'compare_at_price', 'cost_price', 'stock_quantity', 'low_stock_threshold',
            'primary_image', 'condition', 'status',
            'published_at',
        ]
        labels = {
            'name': 'Nombre',
            'slug': 'Slug',
            'short_description': 'Descripción corta',
            'description': 'Descripción',
            'category': 'Categoría',
            'brand': 'Marca',
            'model': 'Modelo',
            'sku': 'SKU',
            'price': 'Precio',
            'compare_at_price': 'Precio de comparación',
            'cost_price': 'Costo',
            'stock_quantity': 'Cantidad en stock',
            'low_stock_threshold': 'Umbral de bajo stock',
            'specifications': 'Especificaciones (JSON)',
            'primary_image': 'Imagen principal',
            'condition': 'Condición',
            'status': 'Estado',
            
            'published_at': 'Fecha de publicación',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure 'features' is not present in the form fields
        if 'features' in self.fields:
            self.fields.pop('features')
        # Add bootstrap classes to widgets
        for name, field in self.fields.items():
            widget = field.widget
            existing = widget.attrs.get('class', '')
            # checkbox and boolean inputs use different classes
            if isinstance(widget, (forms.CheckboxInput,)):
                widget.attrs['class'] = (existing + ' form-check-input').strip()
            else:
                widget.attrs['class'] = (existing + ' form-control').strip()
        # Populate specifications_text from instance.specifications if editing
        instance = kwargs.get('instance')
        if instance and getattr(instance, 'specifications', None):
            specs = instance.specifications
            if isinstance(specs, dict):
                lines = []
                for k, v in specs.items():
                    lines.append(f"{k}: {v}")
                self.fields['specifications_text'].initial = "\n".join(lines)

    def _parse_specifications_text(self, text: str):
        result = {}
        if not text:
            return result
        for raw in text.splitlines():
            line = raw.strip()
            if not line:
                continue
            if ':' in line:
                key, val = line.split(':', 1)
            elif '=' in line:
                key, val = line.split('=', 1)
            else:
                # single value, use as key with empty value
                key, val = line, ''
            key = key.strip()
            val = val.strip()
            # Try to convert numeric values
            if val.isdigit():
                parsed = int(val)
            else:
                try:
                    parsed = float(val)
                except Exception:
                    parsed = val
            result[key] = parsed
        return result

    def save(self, commit=True):
        # Convert specifications_text into dict and assign to instance.specifications
        instance = super().save(commit=False)
        specs_text = self.cleaned_data.get('specifications_text')
        instance.specifications = self._parse_specifications_text(specs_text)
        if commit:
            instance.save()
        return instance


class UserForm(forms.ModelForm):
    password = forms.CharField(required=False, label='Contraseña', widget=forms.PasswordInput, help_text='Dejar en blanco para mantener la contraseña actual')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
        labels = {
            'username': 'Usuario',
            'email': 'Correo electrónico',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'is_active': 'Activo',
            'is_staff': 'Staff',
            'is_superuser': 'Superusuario',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        pwd = self.cleaned_data.get('password')
        if pwd:
            user.set_password(pwd)
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            widget = field.widget
            existing = widget.attrs.get('class', '')
            if isinstance(widget, (forms.CheckboxInput,)):
                widget.attrs['class'] = (existing + ' form-check-input').strip()
            else:
                widget.attrs['class'] = (existing + ' form-control').strip()


class OfferForm(forms.ModelForm):
    class Meta:
        from products.models import Offer
        model = Offer
        fields = ['title', 'description', 'image', 'price', 'discount_percentage', 'start_date', 'end_date', 'is_active']
        labels = {
            'title': 'Título',
            'description': 'Descripción',
            'image': 'Imagen',
            'price': 'Precio',
            'discount_percentage': 'Descuento (%)',
            'start_date': 'Fecha de inicio',
            'end_date': 'Fecha de fin',
            'is_active': 'Activo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            widget = field.widget
            existing = widget.attrs.get('class', '')
            if isinstance(widget, (forms.CheckboxInput,)):
                widget.attrs['class'] = (existing + ' form-check-input').strip()
            else:
                widget.attrs['class'] = (existing + ' form-control').strip()
