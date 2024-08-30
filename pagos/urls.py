from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_pagos, name='listar_pagos'),
    path('crear/', views.crear_pago, name='crear_pago'),
    path('editar/<int:pago_id>/', views.editar_pago, name='editar_pago'),
    path('eliminar/<int:pago_id>/', views.eliminar_pago, name='eliminar_pago'),
]
