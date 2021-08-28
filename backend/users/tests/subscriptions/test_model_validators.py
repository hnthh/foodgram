import pytest
from django.db.utils import IntegrityError
from users.models import Subscribe


def test_self_subscribe(db, user):

    with pytest.raises(
        IntegrityError,
        match='CHECK constraint failed: user_not_author',
    ):
        Subscribe.objects.create(
            user=user,
            author=user,
        )
