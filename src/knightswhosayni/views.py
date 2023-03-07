from django.shortcuts import get_object_or_404, render
from .forms import UserForm
from .models import Key, License, Project


def view_project(request, project_slug, key_slug):
    project = get_object_or_404(Project, slug=project_slug)
    key = get_object_or_404(Key, project=project, slug=key_slug)
    return buy_license(request, key)


def view_key(request, slug):
    key = get_object_or_404(Key, slug=slug)
    return buy_license(request, key)


def buy_license(request,  key):
    url = request.get_full_path()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            code = 'foo'
            days = 7
            license = License(key=key, user=user, code=code, days=days)
            license.save()
    return render(
        request,
        'knightswhosayni/project.html',
        locals(),
    )
