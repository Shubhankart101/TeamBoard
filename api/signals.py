import secrets
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Company


@receiver(post_save, sender=User)
def create_company_profile(sender, instance, created, **kwargs):
    # Detect user first creation (using created / instance._state.adding)
    if created or getattr(getattr(instance, '_state', None), 'adding', False):
        Company.objects.create(
            user=instance,
            company_name=instance.email or instance.username,
            api_key=secrets.token_urlsafe(32)
        )
