from django.db.models.signals import pre_save
from django.dispatch import receiver

from recipes.models import Tag


@receiver(pre_save, sender=Tag)
def clean_fields(sender, instance, *args, **kwargs):
    instance.full_clean()
