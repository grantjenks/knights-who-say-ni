import pytest
from knightswhosayni.models import Key, License, Project


@pytest.mark.django_db
def test_ni():
    project = Project(name='Django Rrweb', slug='django-rrweb')
    project.save()
    assert project

    key = Key(
        project=project,
        value='b5f570e0-6585-402c-b344-3d0521dc8740',
        prefix='DJANGO_RRWEB_',
    )
    key.save()
    assert key

    license = License(
        key=key,
        user='tester',
        code='012-345-678-abc-def',
        days=0,
    )
    license.save()
    assert license
