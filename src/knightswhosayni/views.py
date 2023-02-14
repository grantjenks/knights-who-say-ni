from django.shortcuts import get_object_or_404, render
from .models import Project


def project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(
        request,
        'knightswhosayni/project.html',
        {'project': project},
    )
