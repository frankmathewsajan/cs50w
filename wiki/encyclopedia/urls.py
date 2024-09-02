from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.display, name='display'),
    path("search", views.search, name='search'),
    path("new", views.new, name='new'),
    path("lucky", views.lucky, name='lucky'),
    path("edit", views.edit, name='edit'),
    path("edit/<str:title>", views.edit, name='edit')
]
