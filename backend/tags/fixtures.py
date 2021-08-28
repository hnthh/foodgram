import pytest
from django.core.management import call_command


@pytest.fixture()
def tag(factory):
    return factory.tag()


@pytest.fixture()
def tags(factory):
    return factory.tags()


@pytest.fixture()
def create_tags_command_exec():
    return call_command('create_tags')
