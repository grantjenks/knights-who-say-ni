from django.shortcuts import get_object_or_404, render


def project(request, name):
    project = get_object_or_404(Project, name=name)
    return render('knightswhosayni/project.html')
