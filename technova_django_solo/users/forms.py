from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'confirm_password')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este email ya está registrado")
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres")
        if not re.search(r'\d', password):
            raise ValidationError("La contraseña debe contener al menos un número")
        if not re.search(r'[A-Za-z]', password):
            raise ValidationError("La contraseña debe contener al menos una letra")
        return password
    
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError("Las contraseñas no coinciden")
        return confirm_password
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = False  # El usuario no estará activo hasta que verifique su email
        if commit:
            user.save()
        return user
