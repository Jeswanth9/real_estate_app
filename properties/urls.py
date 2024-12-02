from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('add/', views.add_property, name='add_property'),
    path('<int:pk>/', views.property_detail, name='property_detail'),
    path('<int:pk>/edit/', views.edit_property, name='edit_property'),
    path('<int:pk>/delete/', views.delete_property, name='delete_property'),
    path('preferences/', views.set_preferences, name='set_preferences'),
    path('calculator/', views.calculator, name='calculator'),
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
]