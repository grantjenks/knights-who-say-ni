from django.urls import path

from . import views

urlpatterns = [
    path('<slug>/', views.view_key),
    path('<project_slug>/<key_slug>/', views.view_project),
]
