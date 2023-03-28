from knightswhosayni.models import Key, License, Project

project = Project(name='Django Rrweb', slug='django-rrweb')
project.save()

key = Key(
    project=project,
    value='b5f570e0-6585-402c-b344-3d0521dc8740',
    prefix='DJANGO_RRWEB_',
)
key.save()
