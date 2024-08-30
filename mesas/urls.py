from django.urls import path
from .views import listar_mesas, crear_mesa, actualizar_mesa, eliminar_mesa

urlpatterns = [
    path('', listar_mesas, name='listar_mesas'),
    path('crear/', crear_mesa, name='crear_mesa'),
    path('actualizar/<int:mesa_id>/', actualizar_mesa, name='actualizar_mesa'),
    path('eliminar/<int:mesa_id>/', eliminar_mesa, name='eliminar_mesa'),
]
