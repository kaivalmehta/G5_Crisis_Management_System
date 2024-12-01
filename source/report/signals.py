# signals.py
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Crisis

@receiver(post_save, sender=Crisis)
def send_email_notification(sender, instance, created, **kwargs):
    if created:
        subject = f"New Crisis Reported: {instance.name}"
        message = f"""
        A new Crisis has been reported:
        Title: {instance.name}
        Description: {instance.description}
        Latitude: {instance.lat}
        Longitude: {instance.lon}
        """
        User = get_user_model()
        recipient_list = User.objects.filter(is_active=True).values_list('email', flat=True)
        send_mail(subject, message, 'jashshah780@gmail.com', recipient_list)
