# usuarios/urls.py
from django.urls import path
from .views import profile_view, create_profile, create_user, user_list, listar_clientes, editar_cliente, eliminar_cliente

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('profile/create/', create_profile, name='create_profile'),
    path('create/', create_user, name='create'),
    path('list/', user_list, name='user_list'),
    path('clientes/', listar_clientes, name='listar_clientes'),
    path('clientes/<int:cliente_id>/editar/', editar_cliente, name='editar_cliente'),
    path('clientes/<int:cliente_id>/eliminar/', eliminar_cliente, name='eliminar_cliente'),
]