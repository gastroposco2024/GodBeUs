from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Pedido, ItemPedido, PedidoDomicilio, ItemPedidoDomicilio
from .forms import CrearPedidoForm, AgregarPlatoPedidoForm, FinalizarVentaForm,FinalizarVentaDomicilioForm, EditarPlatoForm,EditarPlatoDomicilioForm, EliminarPlatoForm, EliminarPlatoDomicilioForm,CompraForm, CompraDomicilioForm, CrearPedidoFormDomicilio
from ventas.models import Compra, CompraDetalle, CompraDomicilio, CompraDetalleDomicilio
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.utils.dateparse import parse_datetime
from django.conf import settings
from django.utils.timezone import now
from django.contrib import messages
from mesas.models import Mesa
from platos.models import Plato, Categoria
from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.db.models import Sum, Count, F
from collections import defaultdict
import json
import calendar
from decimal import Decimal
from django.db.models.functions import ExtractMonth
from django.http import JsonResponse
from django.urls import reverse
from usuarios.models import Profile, Cliente
from django.core.paginator import Paginator
from inventario.models import Producto, PlatoProducto
from django.utils import timezone
from django.utils.dateparse import parse_date
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO 
from decimal import Decimal
import pdfkit
from django.template.loader import render_to_string

def buscar_cliente_por_documento(request):
    documento = request.GET.get('documento', None)
    if documento:
        cliente = Cliente.objects.filter(documento=documento).first()
        if cliente:
            data = {
                'doc_cliente': cliente.documento,
                'nombre_cliente': cliente.nombre,
                'telefono_cliente': cliente.telefono,
                'direccion_cliente': cliente.direccion,
            }
            return JsonResponse(data)
    return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

@login_required(login_url='/login/')
def buscar_clientes(request):
    term = request.GET.get('term', '')
    user = request.user  # Obtener el usuario actual desde el request

    # Filtro por documento o nombre
    clientes = Cliente.objects.filter(
        usuario=user,
        documento__icontains=term
    ) | Cliente.objects.filter(
        usuario=user,
        nombre__icontains=term
    )

    # Eliminar duplicados y ordenar resultados si es necesario
    clientes = clientes.distinct()

    results = [{'id': cliente.id, 'nombre': cliente.nombre, 'telefono': cliente.telefono, 'direccion': cliente.direccion, 'documento': cliente.documento} for cliente in clientes]
    return JsonResponse(results, safe=False)

def home(request):
    return render(request, 'pedidos/home.html')

@login_required(login_url='/login/')
def crear_pedido(request):
    if request.method == 'POST':
        # Manejar el formulario de pedido normal (por mesa)
        form_pedido = CrearPedidoForm(request.POST, user=request.user)
        if form_pedido.is_valid():
            mesa = form_pedido.cleaned_data['mesa']
            pedido_existente = Pedido.objects.filter(mesa=mesa, usuario=request.user).first()
            if pedido_existente:
                return redirect('agregar_plato_pedido', pedido_id=pedido_existente.id)

            pedido = Pedido.objects.create(usuario=request.user, mesa=mesa)
            mesa.estado = 'Ocupada'
            mesa.save()

            return redirect('agregar_plato_pedido', pedido_id=pedido.id)
        
        # Manejar el formulario de pedido de domicilio
        form_domicilio = CrearPedidoFormDomicilio(request.POST)
        if form_domicilio.is_valid():
            pedido_domicilio = form_domicilio.save(commit=False)
            pedido_domicilio.usuario = request.user
            pedido_domicilio.save()
            pedido_domicilio_id = pedido_domicilio.id
            return redirect('agregar_plato_pedido_domicilio', pedido_id=pedido_domi.id)

    else:
        form_pedido = CrearPedidoForm(user=request.user)
        form_domicilio = CrearPedidoFormDomicilio()

    # Contexto para la plantilla
    pedidos_activos = Pedido.objects.filter(usuario=request.user)
    pedidos_activos_domicilios = PedidoDomicilio.objects.filter(usuario=request.user)
    mesas = Mesa.objects.filter(usuario=request.user, estado='Libre').order_by('numero')
    mesas_ocupada = Mesa.objects.filter(usuario=request.user, estado='Ocupada')
    profile = Profile.objects.get(user=request.user)

    # Crear una lista de tuplas para almacenar los items de cada pedido de domicilio
    pedidos_con_items = []
    for pedido in pedidos_activos_domicilios:
        items = ItemPedidoDomicilio.objects.filter(pedido=pedido)
        pedidos_con_items.append((pedido, items))

    actualizar_estado_url = reverse('actualizar_estado', args=[0]).replace('0', '')

    return render(request, 'pedidos/crear_pedido.html', {
        'form_pedido': form_pedido,
        'form_domicilio': form_domicilio,
        'pedidos_activos': pedidos_activos,
        'pedidos_activos_domicilios': pedidos_activos_domicilios,
        'mesas': mesas,
        'mesas_ocupada': mesas_ocupada,
        'profile': profile,
        'actualizar_estado_url': actualizar_estado_url,
        'pedidos_con_items': pedidos_con_items
 
    })

def calcular_estado_tiempo(fecha_pedido):
    tiempo_transcurrido = now() - fecha_pedido
    print(tiempo_transcurrido)
    if tiempo_transcurrido < timedelta(minutes=30):  # Puedes ajustar estos valores según sea necesario
        return 'Pendiente'
    elif tiempo_transcurrido < timedelta(hours=1):
        return 'En camino'
    else:
        return 'Entregado'

def actualizar_estado(request, pedido_id):
    try:
        pedido = PedidoDomicilio.objects.get(id=pedido_id)
        fecha_pedido = pedido.fecha_pedido
        estado_tiempo = calcular_estado_tiempo(fecha_pedido)
        estado_tiempo = pedido.estado_pedido  # Asegúrate de que esta propiedad existe
        pedido.save()
        print(estado_tiempo)
        return JsonResponse({'estado_pedido': estado_tiempo})
    except Pedido.DoesNotExist:
        return JsonResponse({'error': 'Pedido no encontrado'}, status=404)

def obtener_pedidos_domicilios(request):
    pedidos_domicilios = PedidoDomicilio.objects.all()
    data = list(pedidos_domicilios.values('id', 'nombre_cliente', 'fecha_pedido', 'direccion_cliente', 'estado_pedido'))
    return JsonResponse(data, safe=False)


@login_required(login_url='/login/')
def crear_pedido_domicilio(request):
    if request.method == 'POST':
        form = CrearPedidoFormDomicilio(request.POST)
        if form.is_valid():
            pedido_domicilio = form.save(commit=False)
            pedido_domicilio.usuario = request.user
            pedido_domicilio.save()
            pedido_domicilio_id = pedido_domicilio.id
            return JsonResponse({'success': True, 'redirect_url': reverse('agregar_plato_pedido_domicilio', args=[pedido_domicilio_id])})
            
        else:
            return JsonResponse({'error': 'Formulario inválido'}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def pedidos_domicilio(request):
    pedidos = PedidoDomicilio.objects.all()
    return render(request, 'pedidos/pedidos_domicilio.html', {'pedidos_domicilio': pedidos})

@login_required(login_url='/login/')
def generar_comanda(request, pedido_id):
    # Obtener el pedido y asegurar que el usuario sea el propietario
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    items = ItemPedido.objects.filter(pedido=pedido)

    # Renderizar la plantilla HTML
    html_string = render_to_string('pedidos/comanda.html', {'pedido': pedido, 'items': items})

    # Configurar pdfkit para usar wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf='/path/to/wkhtmltopdf')  # Asegúrate de que la ruta sea correcta
    
    # Convertir el HTML a PDF
    pdf = pdfkit.from_string(html_string, False, configuration=config)

    # Crear una respuesta HTTP con el PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="comanda_{pedido_id}.pdf"'
    return response

@login_required(login_url='/login/')
def agregar_plato_pedido(request, pedido_id):
    # Obtener el pedido y asegurar que el usuario sea el propietario
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    
    # Obtener todas las categorías y platos
    categorias = Categoria.objects.filter(usuario=request.user)
    platos_por_categoria = {categoria.nombre: categoria.platos.all() for categoria in categorias}

    # Manejo del término de búsqueda
    search_term = request.GET.get('buscar', '')
    if search_term:
        # Filtrar los platos basados en el término de búsqueda
        platos_por_categoria = {categoria.nombre: categoria.platos.filter(nombre__icontains=search_term) for categoria in categorias}

    # Manejo del formulario
    if request.method == 'POST':
        form = AgregarPlatoPedidoForm(request.POST, user=request.user, search_term=search_term)
        if form.is_valid():
            plato = form.cleaned_data['plato']
            cantidad = form.cleaned_data['cantidad']
            detalle = form.cleaned_data['detalle']
            if cantidad is None or cantidad <= 0:
                return HttpResponse("Cantidad inválida", status=400)

            # Verifica si el plato ya existe en el pedido
            item, created = ItemPedido.objects.get_or_create(pedido=pedido, plato=plato, cantidad= cantidad)
            if not created:
                item.cantidad += cantidad
            else:
                item.cantidad = cantidad
            item.detalle = detalle
            item.save()
            return redirect('agregar_plato_pedido', pedido_id=pedido.id)
    else:
        form = AgregarPlatoPedidoForm(user=request.user, search_term=search_term)

    # Obtener los items actuales en el pedido
    items = ItemPedido.objects.filter(pedido=pedido, estado='En proceso')

    # Contexto para renderizar la plantilla
    context = {
        'form': form,
        'pedido': pedido,
        'items': items,
        'categorias': categorias,  # Asegúrate de pasar las categorías al contexto
        'platos_por_categoria': platos_por_categoria,  # Platos agrupados por categoría
        'query': search_term,
    }
    return render(request, 'pedidos/agregar_plato_pedido.html', context)

@login_required(login_url='/login/')
def agregar_plato_pedido_domicilio(request, pedido_id):
    # Obtener el pedido y asegurar que el usuario sea el propietario
    pedido = get_object_or_404(PedidoDomicilio, id=pedido_id, usuario=request.user)
    
    # Obtener todas las categorías y platos
    categorias = Categoria.objects.filter(usuario=request.user)
    platos_por_categoria = {categoria.nombre: categoria.platos.all() for categoria in categorias}

    # Manejo del término de búsqueda
    search_term = request.GET.get('buscar', '')
    if search_term:
        # Filtrar los platos basados en el término de búsqueda
        platos_por_categoria = {categoria.nombre: categoria.platos.filter(nombre__icontains=search_term) for categoria in categorias}

    # Manejo del formulario
    if request.method == 'POST':
        form = AgregarPlatoPedidoForm(request.POST, user=request.user, search_term=search_term)
        if form.is_valid():
            plato = form.cleaned_data['plato']
            cantidad = form.cleaned_data['cantidad']
            detalle = form.cleaned_data['detalle']
            if cantidad is None or cantidad <= 0:
                return HttpResponse("Cantidad inválida", status=400)

            # Verifica si el plato ya existe en el pedido
            item, created = ItemPedidoDomicilio.objects.get_or_create(pedido=pedido, plato=plato, cantidad= cantidad)
            if not created:
                item.cantidad += cantidad
            else:
                item.cantidad = cantidad
            item.detalle = detalle
            item.save()
            return redirect('agregar_plato_pedido_domicilio', pedido_id=pedido.id)
    else:
        form = AgregarPlatoPedidoForm(user=request.user, search_term=search_term)

    # Obtener los items actuales en el pedido
    items = ItemPedidoDomicilio.objects.filter(pedido=pedido)

    # Contexto para renderizar la plantilla
    context = {
        'form': form,
        'pedido': pedido,
        'items': items,
        'categorias': categorias,  # Asegúrate de pasar las categorías al contexto
        'platos_por_categoria': platos_por_categoria,  # Platos agrupados por categoría
        'query': search_term,
    }
    return render(request, 'pedidos/agregar_plato_pedido_domicilio.html', context)

@login_required(login_url='/login/')
def finalizar_venta(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    compra_id = 0

    if request.method == 'POST':
        form = FinalizarVentaForm(request.POST)
        if form.is_valid():
            tipo_pago = form.cleaned_data['tipo_pago']
            cedula_cliente = form.cleaned_data['cedula_cliente']
            impuesto = form.cleaned_data['impuesto']
            descuento = form.cleaned_data['descuento']
            descuento = Decimal(descuento)

            # Calcular el total del pedido sin impuesto
            total_sin_impuesto = sum(item.plato.precio * item.cantidad for item in pedido.itempedido_set.all())
            total_sin_impuesto = (total_sin_impuesto*descuento/100)
            print(total_sin_impuesto)
            # Crear la compra
            compra = Compra.objects.create(
                usuario=pedido.usuario,
                mesa=pedido.mesa,
                total=total_sin_impuesto,
                tipo_pago=tipo_pago,
                cedula_cliente=cedula_cliente,
                impuesto=impuesto
            )
            compra.total_con_impuesto()
            compra.save()
            compra_id = compra.id

            # Agregar los platos del pedido a la compra
            for item in pedido.itempedido_set.all():
                compra_detalle = CompraDetalle.objects.create(
                    compra=compra,
                    plato=item.plato,
                    cantidad=item.cantidad
                )
                plato = item.plato
                plato_productos = PlatoProducto.objects.filter(plato=plato)
                for plato_producto in plato_productos:
                    producto = plato_producto.producto
                    cantidad_descontar = plato_producto.cantidad_necesaria * item.cantidad
                    if producto.cantidad_disponible >= cantidad_descontar:
                        producto.cantidad_disponible -= cantidad_descontar
                        producto.save()
                    else:
                        mensaje = f'Cantidad insuficiente en {plato.nombre} | {producto.nombre}: {producto.cantidad_disponible} | Cantidad Necesaria: {cantidad_descontar} |. Algunos botones están deshabilitados.'
                        # Volver a la misma página con un mensaje de error
                        return render(request, 'pedidos/finalizar_venta.html', {
                            'form': form,
                            'pedido': pedido,
                            'total': total_sin_impuesto,
                            'compra_id':compra_id,
                            'error': mensaje,
                            'disable_buttons': True  # Añadir este contexto para manejar botones deshabilitados
                        })

            
            mesa = pedido.mesa
            mesa.estado = 'Libre'
            mesa.save()

            # Eliminar el pedido una vez finalizada la compra
            pedido.delete()

            # Redirigir a la vista de impresión de la factura
            return redirect('imprimir_factura', compra_id=compra.id)
    else:
        # Si la solicitud no es POST, inicializamos el formulario y los totales
        form = FinalizarVentaForm()
        total_sin_impuesto = sum(item.plato.precio * item.cantidad for item in pedido.itempedido_set.all())
        total_con_impuesto = total_sin_impuesto

    

    return render(request, 'pedidos/finalizar_venta.html', {
        'form': form,
        'pedido': pedido,
        'total': total_sin_impuesto,
        'total_con_impuesto': total_con_impuesto,
        'compra_id':compra_id
    })

@login_required(login_url='/login/')
def finalizar_venta_domicilio(request, pedido_id):
    pedido = get_object_or_404(PedidoDomicilio, id=pedido_id, usuario=request.user)
    compra_id = 0

    if request.method == 'POST':
        form = FinalizarVentaDomicilioForm(request.POST)
        if form.is_valid():
            tipo_pago = form.cleaned_data['tipo_pago']
            impuesto = form.cleaned_data['impuesto']
            guardar_cliente = form.cleaned_data['guardar_cliente']

            if guardar_cliente:
                # Buscar o crear el cliente
                cliente, created = Cliente.objects.get_or_create(
                    usuario=request.user,
                    documento=pedido.doc_cliente,
                    defaults={
                        'nombre': pedido.nombre_cliente,
                        'telefono': pedido.telefono_cliente,
                        'direccion': pedido.direccion_cliente
                    }
                )
                print(f"Cliente guardado: {cliente}")
            else:
                cliente = None

            # Calcular el total del pedido
            total = sum(item.plato.precio * item.cantidad for item in pedido.itempedidodomicilio_set.all())
            
            # Crear la compra
            compra = CompraDomicilio.objects.create(
                usuario=pedido.usuario,
                cedula_cliente=pedido.doc_cliente,
                nombre_cliente=pedido.nombre_cliente,
                telefono_cliente=pedido.telefono_cliente,
                direccion_cliente=pedido.direccion_cliente,
                total=total,
                tipo_pago=tipo_pago,
                impuesto=impuesto
            )
            compra.total_con_impuesto()
            compra.save()
            compra_id = compra.id

            # Agregar los platos del pedido a la compra
            for item in pedido.itempedidodomicilio_set.all():
                compra_detalle = CompraDetalleDomicilio.objects.create(
                    compra=compra,
                    plato=item.plato,
                    cantidad=item.cantidad
                )
                plato = item.plato
                plato_productos = PlatoProducto.objects.filter(plato=plato)
                for plato_producto in plato_productos:
                    producto = plato_producto.producto
                    cantidad_descontar = plato_producto.cantidad_necesaria * item.cantidad
                    if producto.cantidad_disponible >= cantidad_descontar:
                        producto.cantidad_disponible -= cantidad_descontar

                        producto.save()
                    else:
                        return HttpResponse(f"Stock insuficiente para {plato.nombre}.")             
            
            # Eliminar el pedido una vez finalizada la compra
            pedido.delete()

             # Redirigir a la vista de impresión de la factura
            return redirect('imprimir_factura_domicilio', compra_id=compra.id)
    else:
        form = FinalizarVentaDomicilioForm()
        total = sum(item.plato.precio * item.cantidad for item in pedido.itempedidodomicilio_set.all())
    return render(request, 'pedidos/finalizar_venta_domicilio.html', {'form': form, 'pedido': pedido, 'total': total})

@login_required(login_url='/login/')
def obtener_registros_venta(request):
    cedula = request.GET.get('cedula')
    id = request.GET.get('id')
    fecha = request.GET.get('fecha')

    compras = Compra.objects.filter(usuario=request.user).order_by('-fecha_compra')
    compras_domicilios = CompraDomicilio.objects.filter(usuario=request.user).order_by('-fecha_compra')

    if id:
        compras = compras.filter(id=id)
        compras_domicilios = compras_domicilios.filter(id=id)
    elif cedula:
        compras = compras.filter(cedula_cliente__icontains=cedula)
        compras_domicilios = compras_domicilios.filter(cedula_cliente__icontains=cedula)
    
    if fecha:
        try:
            fecha = datetime.strptime(fecha, '%Y-%m-%d')
            compras = compras.filter(fecha_compra__date=fecha.date())
            compras_domicilios = compras_domicilios.filter(fecha_compra__date=fecha.date())
        except ValueError:
            # Manejar error de formato de fecha si es necesario
            pass

    # Paginación
    paginator_compras = Paginator(compras, 10)  # Muestra 10 compras por página
    paginator_compras_domicilios = Paginator(compras_domicilios, 10)  # Muestra 10 domicilios por página

    page_compras = request.GET.get('page_compras')
    page_compras_domicilios = request.GET.get('page_compras_domicilios')

    try:
        compras_paginated = paginator_compras.page(page_compras)
    except PageNotAnInteger:
        compras_paginated = paginator_compras.page(1)
    except EmptyPage:
        compras_paginated = paginator_compras.page(paginator_compras.num_pages)

    try:
        compras_domicilios_paginated = paginator_compras_domicilios.page(page_compras_domicilios)
    except PageNotAnInteger:
        compras_domicilios_paginated = paginator_compras_domicilios.page(1)
    except EmptyPage:
        compras_domicilios_paginated = paginator_compras_domicilios.page(paginator_compras_domicilios.num_pages)

    return render(request, 'pedidos/obtener_registros_venta.html', {
        'compras': compras_paginated,
        'compras_domicilios': compras_domicilios_paginated,
    })

@login_required(login_url='/login/')
def editar_venta(request, id):
    compra = get_object_or_404(Compra, id=id)
    if request.method == 'POST':
        form = CompraForm(request.POST, instance=compra)
        if form.is_valid():
            form.save()
            compra.total_con_impuesto()
            compra.save()
            return redirect('obtener_registros_venta')  # Redirige a la lista de compras después de guardar
    else:
        form = CompraForm(instance=compra)
    return render(request, 'pedidos/editar_venta.html', {'form': form,'compra':compra})

@login_required(login_url='/login/')
def editar_venta_domicilio(request, id):
    compra = get_object_or_404(CompraDomicilio, id=id)
    if request.method == 'POST':
        form = CompraDomicilioForm(request.POST, instance=compra)
        if form.is_valid():
            form.save()
            compra.total_con_impuesto()
            compra.save()
            return redirect('obtener_registros_venta')  # Redirige a la lista de compras después de guardar
    else:
        form = CompraDomicilioForm(instance=compra)
    return render(request, 'pedidos/editar_venta_domicilio.html', {'form': form,'compra':compra})

@login_required(login_url='/login/')
def listar_pedidos_activos(request):
    pedidos_activos = Pedido.objects.filter(usuario=request.user, itempedido__estado='En proceso').distinct()
    pedidos_domicilio = PedidoDomicilio.objects.filter(
        usuario=request.user,
        itempedidodomicilio__estado='En proceso'
    ).distinct()

    # Dividir los pedidos en grupos de 3
    paginator = Paginator(pedidos_activos, 4)  # 3 pedidos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    paginator_domicilio = Paginator(pedidos_domicilio, 4)  # 3 pedidos por página
    page_number_domicilio = request.GET.get('page_domicilio')
    page_obj_domicilio = paginator_domicilio.get_page(page_number_domicilio)
    
    mesas = Mesa.objects.filter(usuario=request.user, estado='Ocupada')

    # Crear un contexto para cada página
    slides = [
        page_obj.paginator.page(i).object_list
        for i in page_obj.paginator.page_range
    ]

    slides_domicilio = [
        page_obj_domicilio.paginator.page(i).object_list
        for i in page_obj_domicilio.paginator.page_range
    ]

    context = {
        'pedidos_activos': pedidos_activos,
        'pedidos_domicilio': pedidos_domicilio,
        'page_obj': page_obj,
        'page_obj_domicilio': page_obj_domicilio,
        'mesas': Mesa.objects.filter(usuario=request.user, estado='Ocupada'),
        'slides': slides,  # Pasar los datos de cada slide de pedidos activos
        'slides_domicilio': slides_domicilio,  # Pasar los datos de cada slide de pedidos de domicilio
    }

    return render(request, 'pedidos/listar_pedidos_activos.html', context)

@login_required(login_url='/login/')
def detalle_pedido(request, mesa_id):
    pedido = get_object_or_404(Pedido, mesa_id=mesa_id, usuario=request.user)

    if request.method == 'POST':
        if 'editar_plato' in request.POST:
            item_id = request.POST.get('item_id')
            item = get_object_or_404(ItemPedido, id=item_id)
            form = EditarPlatoForm(request.POST, instance=item)
            if form.is_valid():
                form.save()
            return redirect('detalle_pedido',mesa_id=mesa_id)
        elif 'eliminar_plato' in request.POST:
            item_id = request.POST.get('item_id')
            item = get_object_or_404(ItemPedido, id=item_id)
            item.delete()
            return redirect('detalle_pedido',mesa_id=mesa_id)

    context = {
        'pedido': pedido,
        'editar_plato_form': EditarPlatoForm(),
        'eliminar_plato_form': EliminarPlatoForm(),
    }
    platos = Plato.objects.filter(usuario=request.user)

    return render(request, 'pedidos/detalle_pedido.html', {'pedido': pedido, 'platos':platos})

@login_required(login_url='/login/')
def detalle_pedido_domicilio(request, pedido_id):
    pedido = get_object_or_404(PedidoDomicilio, id=pedido_id, usuario=request.user)

    if request.method == 'POST':
        if 'editar_plato_domicilio' in request.POST:
            item_id = request.POST.get('item_id')
            item = get_object_or_404(ItemPedidoDomicilio, id=item_id)
            form = EditarPlatoDomicilioForm(request.POST, instance=item)
            if form.is_valid():
                form.save()
            return redirect('detalle_pedido_domicilio', pedido_id=pedido_id)
        elif 'eliminar_plato_domicilio' in request.POST:
            item_id = request.POST.get('item_id')
            item = get_object_or_404(ItemPedidoDomicilio, id=item_id)
            item.delete()
            return redirect('detalle_pedido_domicilio', pedido_id=pedido_id)

    context = {
        'pedido': pedido,
        'editar_plato_form': EditarPlatoDomicilioForm(),
        'eliminar_plato_form': EliminarPlatoDomicilioForm(),
        'platos': Plato.objects.filter(usuario=request.user),
    }

    return render(request, 'pedidos/detalle_pedido_domicilio.html', context)

def decimal_to_float(d):
    if isinstance(d, Decimal):
        return float(d)
    return d

@login_required(login_url='/login/')
def estadisticas(request):
    usuario = request.user
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Filtrar por fechas si se proporcionan
    if start_date and end_date:
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
        compra_filter = Compra.objects.filter(usuario=usuario, fecha_compra__range=[start_date, end_date])
        compra_detalle_filter = CompraDetalle.objects.filter(compra__usuario=usuario, compra__fecha_compra__range=[start_date, end_date])

        compra_filter_domicilio = CompraDomicilio.objects.filter(usuario=usuario, fecha_compra__range=[start_date, end_date])
        compra_detalle_filter_domicilio = CompraDetalleDomicilio.objects.filter(compra__usuario=usuario, compra__fecha_compra__range=[start_date, end_date])

    else:
        compra_filter = Compra.objects.filter(usuario=usuario)
        compra_detalle_filter = CompraDetalle.objects.filter(compra__usuario=usuario)
        compra_filter_domicilio = CompraDomicilio.objects.filter(usuario=usuario)
        compra_detalle_filter_domicilio = CompraDetalleDomicilio.objects.filter(compra__usuario=usuario)


    # Total de ventas
    total_ventas = compra_filter.aggregate(total=Sum('total'))['total'] or 0
    total_ventas_domicilio = compra_filter_domicilio.aggregate(total=Sum('total'))['total'] or 0

    # Ventas por tipo de pago
    ventas_por_tipo_pago = compra_filter.values('tipo_pago').annotate(total=Sum('total'))
    ventas_por_tipo_pago_dict = {compra['tipo_pago']: float(compra['total']) for compra in ventas_por_tipo_pago}
    ventas_por_tipo_pago_domicilio = compra_filter_domicilio.values('tipo_pago').annotate(total=Sum('total'))
    ventas_por_tipo_pago_dict_domicilio = {compra['tipo_pago']: float(compra['total']) for compra in ventas_por_tipo_pago_domicilio}

    # Platos más vendidos
    platos_vendidos = compra_detalle_filter.values('plato__nombre').annotate(cantidad_vendida=Sum('cantidad')).order_by('-cantidad_vendida')
    platos_mas_vendidos = {plato['plato__nombre']: plato['cantidad_vendida'] for plato in platos_vendidos}
    platos_vendidos_domicilio = compra_detalle_filter_domicilio.values('plato__nombre').annotate(cantidad_vendida=Sum('cantidad')).order_by('-cantidad_vendida')
    platos_mas_vendidos_domicilio = {plato['plato__nombre']: plato['cantidad_vendida'] for plato in platos_vendidos_domicilio}

    # Total de platos vendidos
    total_platos_vendidos = compra_detalle_filter.aggregate(total=Sum('cantidad'))['total'] or 0
    total_platos_vendidos_domicilio = compra_detalle_filter_domicilio.aggregate(total=Sum('cantidad'))['total'] or 0

    # Ventas por mes
    ventas_por_mes = compra_filter.annotate(month=ExtractMonth('fecha_compra')).values('month').annotate(total=Sum('total'))
    ventas_por_mes_dict = {}
    for compra in ventas_por_mes:
        month = compra['month']
        if 1 <= month <= 12:  # Verificar que el mes esté en el rango válido
            ventas_por_mes_dict[calendar.month_name[month]] = float(compra['total'])

    ventas_por_mes_domicilio = compra_filter_domicilio.annotate(month=ExtractMonth('fecha_compra')).values('month').annotate(total=Sum('total'))
    ventas_por_mes_dict_domicilio = {}
    for compra in ventas_por_mes_domicilio:
        month = compra['month']
        if 1 <= month <= 12:  # Verificar que el mes esté en el rango válido
            ventas_por_mes_dict_domicilio[calendar.month_name[month]] = float(compra['total'])

    context = {
        'total_ventas': total_ventas,
        'ventas_por_tipo_pago': ventas_por_tipo_pago_dict,
        'platos_mas_vendidos': platos_mas_vendidos,
        'total_platos_vendidos': total_platos_vendidos,
        'ventas_por_mes': ventas_por_mes_dict,
        'platos_nombres': json.dumps(list(platos_mas_vendidos.keys())),  # Serializar a JSON
        'platos_cantidades': json.dumps(list(platos_mas_vendidos.values())), # Serializar a JSON
        'tipos_pago': json.dumps(list(ventas_por_tipo_pago_dict.keys())),  # Serializar a JSON
        'ventas_tipos_pago': json.dumps(list(ventas_por_tipo_pago_dict.values())),
        'meses': json.dumps(list(ventas_por_mes_dict.keys())),
        'ventas_meses': json.dumps(list(ventas_por_mes_dict.values())),
        'total_ventas_domicilio': total_ventas_domicilio,                   # DESDE AQUI COMIENZAN LOS CONTEXT DE DOMICILIOS
        'ventas_por_tipo_pago_domicilio': ventas_por_tipo_pago_dict_domicilio,
        'platos_mas_vendidos_domicilio': platos_mas_vendidos_domicilio,
        'total_platos_vendidos_domicilio': total_platos_vendidos_domicilio,
        'ventas_por_mes_domicilio': ventas_por_mes_dict_domicilio,
        'platos_nombres_domicilio': json.dumps(list(platos_mas_vendidos_domicilio.keys())),  # Serializar a JSON
        'platos_cantidades_domicilio': json.dumps(list(platos_mas_vendidos_domicilio.values())), # Serializar a JSON
        'tipos_pago_domicilio_domicilio': json.dumps(list(ventas_por_tipo_pago_dict_domicilio.keys())),  # Serializar a JSON
        'ventas_tipos_pago_domicilio': json.dumps(list(ventas_por_tipo_pago_dict_domicilio.values())),
        'meses_domicilio': json.dumps(list(ventas_por_mes_dict_domicilio.keys())),
        'ventas_meses_domicilio': json.dumps(list(ventas_por_mes_dict_domicilio.values())),
    }

    return render(request, 'pedidos/estadisticas.html', context)

@login_required(login_url='/login/')
def cambiar_estado_item(request, item_id):
    item = get_object_or_404(ItemPedido, id=item_id)
    item.estado = 'Entregado'
    item.save()
    return redirect('listar_pedidos_activos')

@login_required(login_url='/login/')
def cambiar_estado_item_domicilio(request, item_id):
    item = get_object_or_404(ItemPedidoDomicilio, id=item_id)
    item.estado = 'Entregado'
    item.save()
    return redirect('listar_pedidos_activos')

@login_required(login_url='/login/')
def imprimir_factura(request, compra_id):
    # Verificar si el usuario tiene permiso para acceder a esta compra
    compra = get_object_or_404(Compra, id=compra_id, usuario=request.user)
    detalles = CompraDetalle.objects.filter(compra=compra)
    profile = Profile.objects.get(user=request.user)
    
    # Calcular totales
    total_sin_impuesto = sum(detalle.plato.precio * detalle.cantidad for detalle in detalles)
    total_impuesto = compra.total_impuesto
    total_con_impuesto = total_sin_impuesto + total_impuesto

    # Calcular el total por cada detalle
    detalles_con_totales = [
        {
            'plato': detalle.plato,
            'cantidad': detalle.cantidad,
            'precio_unitario': detalle.plato.precio,
            'total_detalle': detalle.plato.precio * detalle.cantidad
        }
        for detalle in detalles
    ]
    
    redirect_url = reverse('crear_pedido')

    # Renderizar una página HTML que se imprimirá
    return render(request, 'pedidos/imprimir_factura.html', {
        'compra': compra,
        'detalles': detalles_con_totales,
        'total_sin_impuesto': total_sin_impuesto,
        'total_impuesto': total_impuesto,
        'total_con_impuesto': total_con_impuesto,
        'profile': profile,
        'redirect_url': redirect_url,
    })

@login_required(login_url='/login/')
def enviar_factura_por_email(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id, usuario=request.user)
    detalles = CompraDetalle.objects.filter(compra=compra)
    
    destinatario = request.GET.get('email', 'direccion@example.com')
    profile = Profile.objects.get(user=request.user)

    # Calcular totales
    total_sin_impuesto = sum(detalle.plato.precio * detalle.cantidad for detalle in detalles)
    total_impuesto = compra.total_impuesto
    total_con_impuesto = total_sin_impuesto + total_impuesto

    # Calcular el total por cada detalle
    detalles_con_totales = [
        {
            'plato': detalle.plato,
            'cantidad': detalle.cantidad,
            'precio_unitario': detalle.plato.precio,
            'total_detalle': detalle.plato.precio * detalle.cantidad
        }
        for detalle in detalles
    ]

    # Renderizar el HTML de la factura
    html_content = render_to_string('pedidos/imprimir_factura.html', {
        'compra': compra,
        'detalles': detalles_con_totales,
        'total_sin_impuesto': total_sin_impuesto,
        'total_impuesto': total_impuesto,
        'total_con_impuesto': total_con_impuesto,
        'profile': request.user.profile,
    })
    
    pdf_file = BytesIO()
    pisa.CreatePDF(BytesIO(html_content.encode('utf-8')), dest=pdf_file)
    pdf_file.seek(0)

    # Configurar el email
    email = EmailMessage(
        f'Factura de Venta - { profile.company }',
        'Apreciado cliente, Adjunto encontrarás la factura PDF.',
        settings.DEFAULT_FROM_EMAIL,
        [destinatario]
    )
    email.attach('factura.pdf', pdf_file.read(), 'application/pdf')
    email.send()
    messages.success(request, '¡Operación realizada con éxito!')
    return redirect('obtener_registros_venta')

@login_required(login_url='/login/')
def enviar_factura_por_email_domicilio(request, compra_id):
    compra = get_object_or_404(CompraDomicilio, id=compra_id, usuario=request.user)
    detalles = CompraDetalleDomicilio.objects.filter(compra=compra)
    
    destinatario = request.GET.get('email', 'direccion@example.com')

    # Calcular totales
    total_sin_impuesto = sum(detalle.plato.precio * detalle.cantidad for detalle in detalles)
    total_impuesto = compra.total_impuesto
    total_con_impuesto = total_sin_impuesto + total_impuesto

    # Calcular el total por cada detalle
    detalles_con_totales = [
        {
            'plato': detalle.plato,
            'cantidad': detalle.cantidad,
            'precio_unitario': detalle.plato.precio,
            'total_detalle': detalle.plato.precio * detalle.cantidad
        }
        for detalle in detalles
    ]

    # Renderizar el HTML de la factura
    html_content = render_to_string('pedidos/imprimir_factura_domicilio.html', {
        'compra': compra,
        'detalles': detalles_con_totales,
        'total_sin_impuesto': total_sin_impuesto,
        'total_impuesto': total_impuesto,
        'total_con_impuesto': total_con_impuesto,
        'profile': request.user.profile,
    })
    
    pdf_file = BytesIO()
    pisa.CreatePDF(BytesIO(html_content.encode('utf-8')), dest=pdf_file)
    pdf_file.seek(0)

    # Configurar el email
    email = EmailMessage(
        'Factura de Compra',
        'Adjunto encontrarás la factura en formato PDF.',
        settings.DEFAULT_FROM_EMAIL,
        [destinatario]
    )
    email.attach('factura.pdf', pdf_file.read(), 'application/pdf')
    email.send()
    messages.success(request, '¡Operación realizada con éxito!')
    return redirect('obtener_registros_venta')

@login_required(login_url='/login/')
def imprimir_comanda_pedido(request, pedido_id):
    # Verificar si el usuario tiene permiso para acceder a esta compra
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    detalles = ItemPedido.objects.filter(pedido=pedido, estado='En proceso')
    profile = Profile.objects.get(user=request.user)
    
    
    redirect_url = reverse('crear_pedido')

    # Renderizar una página HTML que se imprimirá
    return render(request, 'pedidos/imprimir_comanda.html', {
        'pedido': pedido,
        'detalles': detalles,
        'profile': profile,
        'redirect_url': redirect_url,
    })

@login_required(login_url='/login/')
def imprimir_comanda_pedido_domi(request, pedido_id):
    # Verificar si el usuario tiene permiso para acceder a esta compra
    pedido = get_object_or_404(PedidoDomicilio, id=pedido_id, usuario=request.user)
    detalles = ItemPedidoDomicilio.objects.filter(pedido=pedido, estado='En proceso')
    profile = Profile.objects.get(user=request.user)
    
    
    redirect_url = reverse('crear_pedido')

    # Renderizar una página HTML que se imprimirá
    return render(request, 'pedidos/imprimir_comanda_domi.html', {
        'pedido': pedido,
        'detalles': detalles,
        'profile': profile,
        'redirect_url': redirect_url,
    })

@login_required(login_url='/login/')
def imprimir_factura_domicilio(request, compra_id):
    # Verificar si el usuario tiene permiso para acceder a esta compra
    compra = get_object_or_404(CompraDomicilio, id=compra_id, usuario=request.user)
    detalles = CompraDetalleDomicilio.objects.filter(compra=compra)
    profile = Profile.objects.get(user=request.user)
    
    # Calcular totales
    total_sin_impuesto = sum(detalle.plato.precio * detalle.cantidad for detalle in detalles)
    total_impuesto = compra.total_impuesto
    total_con_impuesto = total_sin_impuesto + total_impuesto

    # Calcular el total por cada detalle
    detalles_con_totales = [
        {
            'plato': detalle.plato,
            'cantidad': detalle.cantidad,
            'precio_unitario': detalle.plato.precio,
            'total_detalle': detalle.plato.precio * detalle.cantidad
        }
        for detalle in detalles
    ]

    redirect_url = reverse('crear_pedido')

    # Renderizar una página HTML que se imprimirá
    return render(request, 'pedidos/imprimir_factura_domicilio.html', {
        'compra': compra,
        'detalles': detalles_con_totales,
        'total_sin_impuesto': total_sin_impuesto,
        'total_impuesto': total_impuesto,
        'total_con_impuesto': total_con_impuesto,
        'profile': profile,
        'redirect_url': redirect_url,
    })

@login_required(login_url='/login/')
def pedidos_actualizados(request):
    last_update_time = request.GET.get('last_update', None)
    
    if last_update_time:
        last_update_time = parse_datetime(last_update_time)
        if last_update_time is None:
            # Manejo de errores si el parsing falla
            last_update_time = timezone.make_aware(timezone.datetime.min)
        elif last_update_time.tzinfo is None:
            last_update_time = timezone.make_aware(last_update_time)
    else:
        last_update_time = timezone.make_aware(timezone.datetime.min)

    pedidos = ItemPedido.objects.filter(
        pedido__usuario=request.user,
        estado='En proceso',
        created_at__gt=last_update_time,
        notificado=False
    )

    
    data = list(pedidos.values('id', 'pedido_id', 'plato__nombre', 'producto__nombre', 'cantidad', 'detalle', 'estado', 'created_at'))
    
    pedidos.update(notificado=True)

    return JsonResponse({'pedidos': data})