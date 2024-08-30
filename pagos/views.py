from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pago
from .forms import PagoForm  # Asegúrate de que el formulario PagoForm esté definido en forms.py
from datetime import datetime, timedelta
from inventario.models import Producto


@login_required(login_url='/login/')
def listar_pagos(request):
    fecha = request.GET.get('fecha')
    concepto = request.GET.get('concepto')

    pagos = Pago.objects.filter(usuario=request.user).order_by('-fecha')

    if fecha:
        try:
            fecha = datetime.strptime(fecha, '%Y-%m-%d')
            pagos = pagos.filter(fecha__date=fecha.date())
        except ValueError:
            # Manejar error de formato de fecha si es necesario
            pass
    
    if concepto:
        pagos = pagos.filter(concepto=concepto)
    
    # Paginación
    paginator = Paginator(pagos, 8)  # Muestra 10 pagos por página
    page = request.GET.get('page')
    try:
        pagos_paginated = paginator.page(page)
    except PageNotAnInteger:
        pagos_paginated = paginator.page(1)
    except EmptyPage:
        pagos_paginated = paginator.page(paginator.num_pages)

    conceptos = Pago.objects.filter(usuario=request.user).values_list('concepto', flat=True).distinct()

    return render(request, 'pagos/listar_pagos.html', {
        'pagos': pagos_paginated,
        'conceptos': conceptos,
    })

@login_required
def crear_pago(request):
    if request.method == 'POST':
        form = PagoForm(request.POST, request.FILES)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.usuario = request.user  # Asocia el pago con el usuario autenticado
            pago.save()
            # Procesar los productos seleccionados
            productos = []
            for key, value in request.POST.items():
                if key.startswith('productos['):  # Detectar todos los campos relacionados con 'productos'
                    index, field_name = key.split('][')  # Separar el índice y el nombre del campo
                    index = index.replace('productos[', '')  # Obtener el índice
                    field_name = field_name.replace(']', '')  # Obtener el nombre del campo ('id' o 'cantidad')
                    
                    # Organizar los datos de productos en un diccionario
                    if len(productos) <= int(index):
                        productos.append({'id': None, 'cantidad': None})  # Añadir un nuevo diccionario para cada producto

                    productos[int(index)][field_name] = value  # Asignar los valores a cada producto

            # Mostrar los productos procesados para verificar
            print(productos)

            # Actualizar cantidades de productos
            for producto_data in productos:
                producto_id = producto_data.get('id')
                cantidad_agregar = int(producto_data.get('cantidad', 0))

                # Verificar y actualizar la cantidad del producto
                if producto_id and cantidad_agregar > 0:
                    producto = get_object_or_404(Producto, id=producto_id, usuario=request.user)
                    producto.cantidad_disponible += cantidad_agregar
                    producto.save()

            messages.success(request, 'Pago registrado exitosamente.')
            return redirect('listar_pagos')  # Redirige a la vista de lista de pagos
    else:
        form = PagoForm()

    productos = Producto.objects.filter(usuario=request.user).order_by('nombre')
    return render(request, 'pagos/crear_pago.html', {'form': form, 'productos':productos})



@login_required
def editar_pago(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id, usuario=request.user)  # Solo permite editar pagos del usuario autenticado
    if request.method == 'POST':
        form = PagoForm(request.POST, request.FILES, instance=pago)
        if form.is_valid():
            # Procesar los productos seleccionados
            productos = []
            for key, value in request.POST.items():
                if key.startswith('productos['):  # Detectar todos los campos relacionados con 'productos'
                    index, field_name = key.split('][')  # Separar el índice y el nombre del campo
                    index = index.replace('productos[', '')  # Obtener el índice
                    field_name = field_name.replace(']', '')  # Obtener el nombre del campo ('id' o 'cantidad')
                    
                    # Organizar los datos de productos en un diccionario
                    if len(productos) <= int(index):
                        productos.append({'id': None, 'cantidad': None})  # Añadir un nuevo diccionario para cada producto

                    productos[int(index)][field_name] = value  # Asignar los valores a cada producto

            # Mostrar los productos procesados para verificar
            print(productos)

            # Actualizar cantidades de productos
            for producto_data in productos:
                producto_id = producto_data.get('id')
                cantidad_agregar = int(producto_data.get('cantidad', 0))

                # Verificar y actualizar la cantidad del producto
                if producto_id and cantidad_agregar > 0:
                    producto = get_object_or_404(Producto, id=producto_id, usuario=request.user)
                    producto.cantidad_disponible += cantidad_agregar
                    producto.save()
            
            form.save()
            messages.success(request, 'Pago actualizado exitosamente.')
            return redirect('listar_pagos')
    else:
        form = PagoForm(instance=pago)
    productos = Producto.objects.filter(usuario=request.user).order_by('nombre')
    return render(request, 'pagos/editar_pago.html', {'form': form, 'pago': pago, 'productos': productos})

@login_required
def eliminar_pago(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id, usuario=request.user)  # Solo permite eliminar pagos del usuario autenticado
    if request.method == 'POST':
        pago.delete()
        messages.success(request, 'Pago eliminado exitosamente.')
        return redirect('listar_pagos')
    return render(request, 'pagos/eliminar_pago.html', {'pago': pago})
