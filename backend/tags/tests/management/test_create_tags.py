import pytest
from tags.models import Tag

pytestmark = [pytest.mark.django_db]


def test_db_should_contain_tags(create_tags_command_exec):
    assert Tag.objects.count() == 3
