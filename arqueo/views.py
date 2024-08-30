from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ArqueoCajaInicial
from .forms import ArqueoCajaForm
from usuarios.models import Profile
from django.utils import timezone
from pagos.choices import ESTADO_FINALIZADO

@login_required(login_url='/login/')
def iniciar_arqueo_caja(request):
    if request.method == 'POST':
        form = ArqueoCajaForm(request.POST)
        if form.is_valid():
            arqueo = form.save(commit=False)
            arqueo.usuario = request.user
            arqueo.calcular_totales()  # Calcula los totales antes de guardar
            arqueo.calcular_total_efectivo()
            arqueo.save()
            return redirect('listar_arqueos')
    else:
        form = ArqueoCajaForm()
    return render(request, 'arqueo_caja/iniciar_arqueo_caja.html', {'form': form})

@login_required(login_url='/login/')
def cerrar_arqueo_caja(request, arqueo_id):
    arqueo = get_object_or_404(ArqueoCajaInicial, id=arqueo_id, usuario=request.user)
    
    if request.method == 'POST':

        form = ArqueoCajaForm(request.POST, instance=arqueo)
        if form.is_valid():
            arqueo = form.save(commit=False)
            arqueo.fecha_fin = timezone.now()  # Establece la fecha de cierre
            arqueo.estado = ArqueoCajaInicial.ESTADO_FINALIZADO
            arqueo.calcular_totales()  # Calcula los totales antes de guardar
            arqueo.calcular_total_efectivo()
            arqueo.save()  # Guarda los cambios
            return redirect('listar_arqueos')
        else:
            print("Formulario no válido")
            print(form.errors)  # Añadido para depurar errores del formulario
    else:
        form = ArqueoCajaForm(instance=arqueo)

    ventas_por_metodo = arqueo.ventas_por_metodo_pago()
    ventas_por_metodo_domicilios = arqueo.ventas_por_metodo_pago_domicilios()
    pagos_por_metodo = arqueo.pagos_por_metodo_pago()

    return render(request, 'arqueo_caja/cerrar_arqueo_caja.html', {
        'form': form,
        'arqueo': arqueo,
        'ArqueoCajaInicial': ArqueoCajaInicial,  # Pasar el modelo al contexto
        'pagos_por_metodo':pagos_por_metodo,
        'ventas_por_metodo': ventas_por_metodo,
        'ventas_por_metodo_domicilios': ventas_por_metodo_domicilios
        
    })

@login_required
def cerrar_arqusseo_caja(request, arqueo_id):
    arqueo = get_object_or_404(ArqueoCajaInicial, id=arqueo_id, usuario=request.user)
    
    if request.method == 'POST':
        form = ArqueoCajaForm(request.POST, instance=arqueo)
        if form.is_valid():
            arqueo = form.save(commit=False)
            arqueo.fecha_fin = timezone.now()  # Establece la fecha de cierre
            arqueo.estado = arqueo.ESTADO_FINALIZADO
            arqueo.calcular_totales()  # Calcula los totales antes de guardar
            arqueo.save()  # Guarda los cambios
            form.save()
            return redirect('listar_arqueos')
    else:
        form = ArqueoCajaForm(instance=arqueo)
    
    return render(request, 'arqueo_caja/cerrar_arqueo_caja.html', {'form': form})

@login_required(login_url='/login/')
def listar_arqueos(request):
    arqueos = ArqueoCajaInicial.objects.filter(usuario=request.user).order_by('-fecha_inicio')
    hay_en_curso = arqueos.filter(estado=ArqueoCajaInicial.ESTADO_EN_CURSO).exists()
    
    return render(request, 'arqueo_caja/listar_arqueos.html', {
        'arqueos': arqueos,
        'hay_en_curso': hay_en_curso,
    })

@login_required(login_url='/login/')
def detalle_arqueo(request, arqueo_id):
    arqueo = get_object_or_404(ArqueoCajaInicial, id=arqueo_id, usuario=request.user)
    profile = Profile.objects.get(user=request.user)

    if arqueo.estado == ArqueoCajaInicial.ESTADO_EN_CURSO:
        arqueo.fecha_fin = timezone.now()
        arqueo.save()
        arqueo.calcular_totales()  # Asegura que los totales estén actualizados si está en curso
        arqueo.calcular_total_efectivo()
    
    total_monedas = (
        arqueo.monedas_1000 * 1000 +
        arqueo.monedas_500 * 500 +
        arqueo.monedas_200 * 200 +
        arqueo.monedas_100 * 100 +
        arqueo.monedas_50 * 50 
  
    )

    total_monedas_cantidad = (
        arqueo.monedas_1000 +
        arqueo.monedas_500 +
        arqueo.monedas_200 +
        arqueo.monedas_100 +
        arqueo.monedas_50 
  
    )

    total_billetes = (
        arqueo.billetes_2000 * 2000 +
        arqueo.billetes_5000 * 5000 +
        arqueo.billetes_10000 * 10000 +
        arqueo.billetes_20000 * 20000 +
        arqueo.billetes_50000 * 50000 +
        arqueo.billetes_100000 * 100000 
  
    )

    total_billetes_cantidad = (
        arqueo.billetes_2000 +
        arqueo.billetes_5000 +
        arqueo.billetes_10000 +
        arqueo.billetes_20000 +
        arqueo.billetes_50000 +
        arqueo.billetes_100000 
  
    )

    ventas_por_metodo = arqueo.ventas_por_metodo_pago()
    ventas_por_metodo_domicilios = arqueo.ventas_por_metodo_pago_domicilios()
    pagos_por_metodo = arqueo.pagos_por_metodo_pago()
    
    return render(request, 'arqueo_caja/detalle_arqueo_caja.html', {
        'arqueo': arqueo,
        'ventas_por_metodo': ventas_por_metodo,
        'pagos_por_metodo': pagos_por_metodo,
        'ventas_por_metodo_domicilios':ventas_por_metodo_domicilios,
        'profile': profile,
        'total_monedas':total_monedas,
        'total_monedas_cantidad':total_monedas_cantidad,
        'total_billetes':total_billetes,
        'total_billetes_cantidad':total_billetes_cantidad
    })

@login_required(login_url='/login/')
def eliminar_arqueo(request, arqueo_id):
    arqueo = get_object_or_404(ArqueoCajaInicial, id=arqueo_id, usuario=request.user)
    if request.method == 'POST':
        arqueo.delete()
        return redirect('listar_arqueos')
    return render(request, 'arqueo_caja/eliminar_arqueo.html', {'arqueo': arqueo})