from django.urls import path

from . import views

urlpatterns = [
    path('browse/', views.BrowseView.as_view(), name='pipelines.browse'),
]
