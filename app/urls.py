from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/<str:tag>', views.upload, name='upload'),
    path('zip/<str:tag>', views.download, name='download')
]