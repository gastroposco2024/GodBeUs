# platos/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PlatoForm, CategoriaForm
from .models import Plato, Categoria

@login_required(login_url='/login/')
def crear_plato(request):
    if request.method == 'POST':
        form = PlatoForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            plato = form.save(commit=False)
            plato.usuario = request.user  # Asignar el usuario actual
            plato.save()
            return redirect('listar_platos')  # Redirige a la lista de platos o donde desees
    else:
        form = PlatoForm(user=request.user)
    return render(request, 'platos/crear_plato.html', {'form': form})

@login_required(login_url='/login/')
def eliminar_plato(request, plato_id):
    plato = get_object_or_404(Plato, pk=plato_id, usuario=request.user)
    if request.method == 'POST':
        plato.delete()
        return redirect('listar_platos')
    return render(request, 'platos/eliminar_plato.html', {'plato': plato})

@login_required(login_url='/login/')
def listar_platos(request):
    categorias = Categoria.objects.filter(usuario=request.user)
    platos_por_categoria = {categoria: categoria.platos.all() for categoria in categorias}
    return render(request, 'platos/listar_platos.html', {'platos_por_categoria': platos_por_categoria})

@login_required(login_url='/login/')
def actualizar_plato(request, plato_id):
    plato = get_object_or_404(Plato, id=plato_id, usuario=request.user)
    if request.method == 'POST':
        form = PlatoForm(request.POST, request.FILES, instance=plato, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('listar_platos')
    else:
        form = PlatoForm(instance=plato, user=request.user)
    return render(request, 'platos/actualizar_plato.html', {'form': form, 'plato': plato})

def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.usuario = request.user
            categoria.save()
            return redirect('listar_platos')
    else:
        form = CategoriaForm()
    return render(request, 'platos/crear_categoria.html', {'form': form})