from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("random", views.randompage, name="random"),
    path("<str:title>/edit", views.edit, name="edit"),
    path("<str:title>", views.page, name="page"),

]
