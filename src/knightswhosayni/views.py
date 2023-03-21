import datetime as dt
import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
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
    product_id = request.GET.get('product_id', '')
    sale_id = request.GET.get('sale_id', '')
    if request.method == 'GET':
        sale = Sale.objects.filter(
            product_id=product_id,
            sale_id=sale_id,
            modify_time__gt=timezone.now() - dt.timedelta(hours=1),
        ).first()
        license = sale and sale.license
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
    payload = {key: value for key, (value,) in payload.items()}
    product_permalink = payload['product_permalink']
    license_user = payload.get('url_params[license_user]')
    license_user = license_user or payload['email']
    product_id = payload['product_id']
    sale_id = payload['sale_id']
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
