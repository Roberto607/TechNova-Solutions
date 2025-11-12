from django.shortcuts import redirect
from django.contrib import messages
from .models import Subscriber

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            subscriber, created = Subscriber.objects.get_or_create(
                email=email,
                defaults={'is_active': True}
            )
            if created:
                messages.success(request, '¡Gracias por suscribirte a nuestro newsletter!')
            else:
                messages.info(request, 'Ya estás suscrito a nuestro newsletter.')
        else:
            messages.error(request, 'Por favor, ingresa un email válido.')
    return redirect('home')
