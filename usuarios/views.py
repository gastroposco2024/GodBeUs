# usuarios/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, ClienteForm
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Cliente
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

@login_required(login_url='/login/')
def profile_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'usuarios/profile.html', {'form': form})

@login_required(login_url='/login/')
def create_profile(request):
    if hasattr(request.user, 'profile'):
        # Si el perfil ya existe, redirige al perfil
        return redirect('profile')

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile')
    else:
        form = ProfileForm()

    return render(request, 'usuarios/create_profile.html', {'form': form})

# Permitir que solo los administradores creen nuevos usuarios
def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Verifica si el perfil ya existe antes de crearlo
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)
            return redirect('user_list')  # Redirige a una página de lista de usuarios o donde prefieras
    else:
        form = UserCreationForm()
    
    return render(request, 'usuarios/create_user.html', {'form': form})

@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.all()
    return render(request, 'usuarios/user_list.html', {'users': users})

@login_required(login_url='/login/')
def listar_clientes(request):
    clientes = Cliente.objects.filter(usuario=request.user)
    formularios = []
    for cliente in clientes:
        form = ClienteForm(instance=cliente)
        formularios.append({'cliente': cliente, 'form': form})
    return render(request, 'clientes/listar_clientes.html', {'formularios': formularios})

@login_required(login_url='/login/')
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id, usuario=request.user)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')  # Redirige a la lista de clientes después de guardar
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'clientes/editar_cliente.html', {'form': form, 'cliente': cliente})

@login_required(login_url='/login/')
def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id, usuario=request.user)
    if request.method == 'POST':
        cliente.delete()
        return redirect('listar_clientes') 
    
    return render(request, 'clientes/eliminar_cliente.html', {'cliente': cliente})