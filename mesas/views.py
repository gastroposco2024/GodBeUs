# mesas/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Mesa
from .forms import MesaForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

@login_required(login_url='/login/')
def listar_mesas(request):
    mesas = Mesa.objects.filter(usuario=request.user).order_by('numero')
    return render(request, 'mesas/lista_mesas.html', {'mesas': mesas})

@login_required(login_url='/login/')
def crear_mesa(request):
    if request.method == 'POST':
        form = MesaForm(request.POST)
        if form.is_valid():
            mesa = form.save(commit=False)
            mesa.usuario = request.user  # Asigna el usuario autenticado a la mesa
            try:
                mesa.save()
                return redirect('listar_mesas')  # Ajusta esto al nombre correcto de la URL para listar las mesas
            except IntegrityError:
                form.add_error('numero', 'Ya existe una mesa con este número para este usuario.')
    else:
        form = MesaForm()
    return render(request, 'mesas/crear_mesa.html', {'form': form})

@login_required(login_url='/login/')
def actualizar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id, usuario=request.user)
    if request.method == 'POST':
        form = MesaForm(request.POST, instance=mesa)
        if form.is_valid():
            form.save()
            return redirect('listar_mesas')
    else:
        form = MesaForm()
    return render(request, 'mesas/actualizar_mesa.html', {'form': form})

@login_required(login_url='/login/')
def eliminar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id, usuario=request.user)
    
    if request.method == 'POST':
        mesa.delete()
        return redirect('listar_mesas')
    
    return render(request, 'mesas/confirmar_eliminar.html', {'mesa': mesa})
