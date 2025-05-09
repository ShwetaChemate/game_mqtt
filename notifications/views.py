from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .mqtt import mqtt_client
from .models import GameEvent


@login_required
def producer_view(request):
    if request.method == 'POST':
        event = request.POST.get('event')
        if event:
            mqtt_client.publish(request.user.username, event)
            return redirect('consumer')  # Redirect after posting

    return render(request, 'notifications/producer.html')


@login_required
def consumer_view(request):
    events = GameEvent.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'notifications/consumer.html', {'events': events})