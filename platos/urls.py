# platos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_platos, name='listar_platos'),
    path('eliminar/<int:plato_id>/', views.eliminar_plato, name='eliminar_plato'),
    path('crear/', views.crear_plato, name='crear_plato'),
    path('platos/actualizar/<int:plato_id>/', views.actualizar_plato, name='actualizar_plato'),
    path('crear-categoria/', views.crear_categoria, name='crear_categoria'),
]
