from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .forms import UserForm
from .models import Key, License, Project
from .utils import keygen


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
            license_user = form.cleaned_data['user']
            days = 7
            code_uuid = keygen(key.value, license_user, days)
            code = str(code_uuid)
            license = License(key=key, user=license_user, code=code, days=days)
            license.save()
    return render(
        request,
        'knightswhosayni/project.html',
        locals(),
    )


def gumroad_webhook(request):
    text = f'{dict(request.GET)!r}\n{dict(request.POST)!r}'
    return HttpResponse(text, content_type="text/plain")
