import secrets
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Company


@receiver(pre_save, sender=User)
def capture_user_adding_state(sender, instance, **kwargs):
    # Django resets _state.adding to False before post_save fires, so capture it here.
    instance._is_first_creation = instance._state.adding


@receiver(post_save, sender=User)
def create_company_profile(sender, instance, **kwargs):
    if getattr(instance, '_is_first_creation', False):
        instance._is_first_creation = False
        Company.objects.create(
            user=instance,
            company_name=instance.email or instance.username,
            api_key=secrets.token_urlsafe(32)
        )
