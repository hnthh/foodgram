from behaviors.behaviors import Timestamped
from django.db import models
from django.db.models import F
from django.db.models.functions import Coalesce

__all__ = [
    'models',
    'DefaultManager',
    'DefaultModel',
    'DefaultQuerySet',
    'TimestampedModel',
]


class DefaultQuerySet(models.QuerySet):
    Q = None

    @classmethod
    def as_manager(cls):
        return DefaultManager.from_queryset(cls)()

    as_manager.queryset_only = True

    def __getattr__(self, name):
        if self.Q is not None and hasattr(self.Q, name):
            return lambda *args: self.filter(getattr(self.Q, name)())

        raise AttributeError()

    def with_last_update(self):
        return self.annotate(last_update=Coalesce(F('modified'), F('created')))


class DefaultManager(models.Manager):
    Q = None

    @classmethod
    def as_manager(cls):
        return DefaultManager.from_queryset(cls)()

    as_manager.queryset_only = True

    def __getattr__(self, name):
        if self.Q is not None and hasattr(self.Q, name):
            return lambda *args: self.filter(getattr(self.Q, name)())

        raise AttributeError()

    def with_last_update(self):
        return self.annotate(last_update=Coalesce(F('modified'), F('created')))


class DefaultModel(models.Model):
    objects = DefaultManager()

    class Meta:
        abstract = True

    def __str__(self):
        if hasattr(self, 'name'):
            return str(self.name)

        return super().__str__()


class TimestampedModel(DefaultModel, Timestamped):

    class Meta:
        abstract = True
