from django import forms
from django.core.validators import RegexValidator
from .models import ContactMessage


name_validator = RegexValidator(
    regex=r"^[A-Za-zÀ-ÖØ-öø-ÿ\s'\-]+$",
    message="El nombre sólo puede contener letras, espacios, apóstrofes y guiones."
)

phone_validator = RegexValidator(
    regex=r'^[0-9+\-\s()]+$',
    message="El teléfono sólo puede contener números, espacios, paréntesis, + y guiones."
)


class ContactForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        validators=[name_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'name',
            'placeholder': 'Ingresa tu nombre'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'email',
            'placeholder': 'tu@email.com'
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        validators=[phone_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'phone',
            'placeholder': '(809) 123-4567'
        })
    )
    subject = forms.ChoiceField(
        choices=ContactMessage.SUBJECT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'subject'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'id': 'message',
            'rows': 6,
            'placeholder': 'Escribe tu mensaje aquí...'
        }),
        max_length=2000
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
