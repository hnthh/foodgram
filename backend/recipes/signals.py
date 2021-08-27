from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save)
def clean_fields(sender, instance, *args, **kwargs):
    instance.full_clean()
