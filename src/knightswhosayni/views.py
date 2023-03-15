import datetime as dt
import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import UserForm
from .models import Key, License, Project, Sale
from .utils import keygen


def view_project(request, project_slug, key_slug):
    project = get_object_or_404(Project, slug=project_slug)
    key = get_object_or_404(Key, project=project, slug=key_slug)
    return buy_license(request, key)


def view_key(request, slug):
    key = get_object_or_404(Key, slug=slug)
    return buy_license(request, key)


def buy_license(request, key):
    url = request.get_full_path()
    if request.method == 'GET':
        product_id = request.GET.get('product_id', '')
        sale_id = request.GET.get('sale_id', '')
        sale = Sale.objects.filter(product_id=product_id, sale_id=sale_id).first()
        license = sale.license if sale else None
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            license_user = form.cleaned_data['user']
            if 'buy' in request.POST:
                return redirect(key.gumroad_link + '?license_user=' + license_user)
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


@csrf_exempt
@require_POST
def gumroad_webhook(request):
    payload = dict(request.POST)
    product_permalink, = payload['product_permalink']
    license_user, = payload['url_params[license_user]']
    product_id, = payload['product_id']
    sale_id, = payload['sale_id']
    key = Key.objects.get(gumroad_link=product_permalink)
    code = str(keygen(key.value, license_user, days=0))
    license = License(key=key, user=license_user, code=code, days=0)
    license.save()
    sale = Sale(
        product_id=product_id,
        sale_id=sale_id,
        payload=payload,
        license=license,
    )
    sale.save()
    return HttpResponse('OK')
