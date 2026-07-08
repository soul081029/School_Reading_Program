from django.urls import path

from . import views

urlpatterns = [
    path('', views.recommendation_list, name='recommendation_list'),
    path('create/', views.create_recommendation, name='create_recommendation'),
    path('<int:id>/', views.recommendation_detail, name='recommendation_detail'),
    path('<int:id>/edit/', views.update_recommendation, name='update_recommendation'),
    path('<int:id>/delete/', views.delete_recommendation, name='delete_recommendation'),
    path('<int:id>/like/', views.toggle_like, name='toggle_like'),
]
