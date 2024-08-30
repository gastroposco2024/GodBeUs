from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, PlatoProducto
from .forms import ProductoForm, AsociarProductoForm
from django.contrib.auth.decorators import login_required
from platos.models import Plato 
from django.db.models import Q

@login_required(login_url='/login/')
def lista_productos(request):
    query = request.GET.get('q', '')

    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        producto = get_object_or_404(Producto, id=producto_id, usuario=request.user)
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            # Create a query string for the redirect
            query_string = QueryDict(mutable=True)
            query_string['q'] = query
            return redirect(f"{request.path}?{query_string.urlencode()}")
    
    productos = Producto.objects.filter(usuario=request.user)
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) |
            Q(cantidad_disponible__icontains=query) |
            Q(precio__icontains=query)
        )

    productos_info = []
    for producto in productos:
        form = ProductoForm(instance=producto)
        productos_info.append({
            'producto': producto,
            'form': form,
            'nombre': form['nombre'].value(),
            'cantidad_disponible': form['cantidad_disponible'].value(),
            'precio': form['precio'].value(),
            'unidad_medida': form['unidad_medida'].value(),
        })
    
    return render(request, 'inventario/lista_productos.html', {'productos_info': productos_info, 'query': query})

@login_required(login_url='/login/')
def actualizar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, usuario=request.user)
    print(f"Producto Precio: {producto.precio}")  # Depuración
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'inventario/actualizar_producto.html', {'form': form})

@login_required(login_url='/login/')
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, usuario=request.user)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'inventario/eliminar_producto.html', {'producto': producto})

@login_required(login_url='/login/')
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.usuario = request.user  # Asigna el usuario actual
            producto.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'inventario/crear_producto.html', {'form': form})

@login_required(login_url='/login/')
def listar_platos(request):
    platos = Plato.objects.filter(usuario=request.user)
    return render(request, 'inventario/listar_platos.html', {'platos': platos})

@login_required(login_url='/login/')
def detalle_plato(request, plato_id):
    plato = get_object_or_404(Plato, id=plato_id, usuario=request.user)
    plato_productos = PlatoProducto.objects.filter(plato=plato)
    return render(request, 'inventario/detalle_plato.html', {'plato': plato, 'plato_productos': plato_productos})

@login_required(login_url='/login/')
def asociar_producto(request, plato_id):
    plato = get_object_or_404(Plato, id=plato_id, usuario=request.user)
    plato_productos = PlatoProducto.objects.filter(plato=plato)

    if request.method == 'POST':
        if 'producto_id' in request.POST:
            producto_id = request.POST.get('producto_id')
            producto = get_object_or_404(Producto, id=producto_id, usuario=request.user)

            # Crear la relación entre el plato y el producto si no existe
            if not PlatoProducto.objects.filter(plato=plato, producto=producto).exists():
                PlatoProducto.objects.create(plato=plato, producto=producto, cantidad_necesaria=1, unidad_medida=producto.unidad_medida)
                return redirect('asociar_producto', plato_id=plato.id)
            else:
                # Manejo de la situación si la asociación ya existe
                pass
        elif 'update' in request.POST:
            plato_producto_id = request.POST.get('plato_producto_id')
            plato_producto = get_object_or_404(PlatoProducto, id=plato_producto_id)
            cantidad_necesaria = request.POST.get('cantidad_necesaria')
            cantidad_necesaria = float(cantidad_necesaria)
            plato_producto.cantidad_necesaria = cantidad_necesaria
            plato_producto.save()
            return redirect('asociar_producto', plato_id=plato.id)
        elif 'delete' in request.POST:
            plato_producto_id = request.POST.get('plato_producto_id')
            plato_producto = get_object_or_404(PlatoProducto, id=plato_producto_id)
            plato_producto.delete()
            return redirect('asociar_producto', plato_id=plato.id)

    productos = Producto.objects.filter(usuario=request.user)
    return render(request, 'inventario/asociar_producto.html', {'plato': plato, 'productos': productos, 'plato_productos': plato_productos})