from django.urls import path

from . import views

urlpatterns = [
    path('browse/', views.BrowseView.as_view(), name='pipelines.browse'),
    path('<pipeline_id>/setup/', views.setup, name='pipeline.setup'),
]
