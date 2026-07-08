from django.urls import path

from . import views

urlpatterns = [
    path('', views.quote_list, name='quote_list'),
    path('create/', views.quote_create, name='quote_create'),
    path('<int:id>/edit/', views.quote_update, name='quote_update'),
    path('<int:id>/delete/', views.quote_delete, name='quote_delete'),
]
