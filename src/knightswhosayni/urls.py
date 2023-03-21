from django.urls import path

from . import views

urlpatterns = [
    path('gumroad-webhook/', views.gumroad_webhook),
    path('email/<sale_id>/', views.view_email),
    path('<slug>/', views.view_key),
    path('<project_slug>/<key_slug>/', views.view_project),
]
