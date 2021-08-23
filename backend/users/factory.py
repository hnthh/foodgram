from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from config.testing import register

User = get_user_model()


@register
def user(self, **kwargs):
    return self.mixer.blend(User, **kwargs)


@register
def anon(self, **kwargs):
    return AnonymousUser()
