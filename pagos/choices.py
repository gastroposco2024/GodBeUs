# myapp/choices.py
METODO_PAGO_CHOICES = [
        ('Efectivo', 'Efectivo'),
        ('Consignación', 'Consignación'),
        ('Transferencia', 'Transferencia'),
        ('Cheque', 'Cheque'),
        ('Tarjeta crédito', 'Tarjeta crédito'),
        ('Tarjeta débito', 'Tarjeta débito'),
    ]
    
CONCEPTO_CATEGORIAS = {
    'Sueldos': [
        ('sueldos_personal_ventas', 'Sueldos personal de ventas'),
        ('horas_extras_recargos', 'Horas extras y recargos personal de ventas'),
        ('comisiones_personal_ventas', 'Comisiones personal de ventas'),
        ('auxilio_transporte', 'Auxilio de transporte personal de ventas'),
        ('cesantias_personal_ventas', 'Cesantías personal de ventas'),
        ('intereses_cesantias', 'Intereses sobre cesantías personal de ventas'),
        ('prima_servicios', 'Prima de servicios personal de ventas'),
        ('vacaciones_personal_ventas', 'Vacaciones personal de ventas'),
        ('dotacion_trabajadores', 'Dotación a trabajadores de ventas'),
        ('aportes_arl', 'Aportes a ARL personal de ventas'),
        ('aportes_eps', 'Aportes a EPS personal de ventas'),
        ('aportes_fondo_pensiones_cesantias', 'Aportes fondo de pensiones y cesantías personal de ventas'),
        ('aportes_cajas_compensacion', 'Aportes cajas de compensación familiar personal de ventas'),
        ('aportes_icbf', 'Aportes ICBF personal de ventas'),
        ('aportes_sena', 'Aportes SENA personal de ventas'),
    ],
    'Gastos_Operativos': [
        ('gastos_administracion', 'Gastos de administración'),
        ('gastos_personal', 'Gastos de personal'),
        ('sueldos_salarios', 'Sueldos y salarios'),
        ('horas_extras_recargos', 'Horas extras y recargos'),
        ('comisiones', 'Comisiones'),
        ('auxilio_transporte', 'Auxilio de transporte'),
        ('cesantias', 'Cesantías'),
        ('intereses_cesantias', 'Intereses sobre cesantías'),
        ('prima_servicios', 'Prima de servicios'),
        ('vacaciones', 'Vacaciones'),
        ('dotacion_trabajadores', 'Dotación a trabajadores'),
        ('aportes_arl', 'Aportes a ARL'),
        ('aportes_eps', 'Aportes a EPS'),
        ('aportes_fondo_pensiones_cesantias', 'Aportes fondo de pensiones y cesantías'),
        ('aportes_cajas_compensacion', 'Aportes cajas de compensación familiar'),
        ('aportes_icbf', 'Aportes ICBF'),
        ('aportes_sena', 'Aportes SENA'),
    ],
    'Gastos_Generales': [
        ('servicios_publicos', 'Servicios públicos'),
        ('gas', 'Gas'),
        ('aseo', 'Aseo'),
        ('agua', 'Agua'),
        ('energia_electrica', 'Energía eléctrica'),
        ('telefono_internet', 'Teléfono / Internet'),
        ('transporte_acarreo', 'Transporte y acarreo'),
        ('otros_servicios', 'Otros servicios'),
    ],
    'Gastos_Representacion_Publicidad': [
        ('propaganda_publicidad', 'Propaganda y publicidad'),
        ('elementos_aseo', 'Elementos de aseo y cafetería'),
        ('utiles_papeleria', 'Útiles, papelería y fotocopia'),
        ('combustibles_lubricantes', 'Combustibles y lubricantes'),
        ('taxis_buses', 'Taxis y buses'),
        ('estacionamiento', 'Estacionamiento'),
    ],
    'Mantenimiento_Reparaciones': [
        ('mantenimiento_reparaciones', 'Mantenimiento y reparaciones'),
        ('construccion_edificacion', 'Construcción y edificación'),
    ],
    'Activos_Pasivos': [
        ('caja', 'Caja'),
        ('efectivo_equivalentes', 'Efectivo y equivalentes de efectivo'),
        ('bancos', 'Bancos'),
        ('inventario_mercancias', 'Inventario de mercancías'),
        ('propiedad_planta_equipo', 'Propiedad, planta y equipo'),
        ('terrenos', 'Terrenos'),
        ('construcciones_edificaciones', 'Construcciones y edificaciones'),
        ('equipo_oficina', 'Equipo de oficina'),
        ('muebles_enseres', 'Muebles y enseres'),
        ('equipo_computacion', 'Equipo de computación'),
        ('vehiculos', 'Vehículos'),
        ('depreciacion_acumulada', 'Depreciación acumulada'),
    ],
    'Impuestos_Retenciones': [
        ('impuestos_por_pagar', 'Impuestos por pagar'),
        ('impuesto_ventas_por_pagar', 'Impuesto a las ventas por pagar'),
        ('iva_devenido_compras', 'IVA devuelto en compras'),
        ('iva_devuelto_ventas', 'IVA devuelto en ventas'),
        ('impuesto_industria_comercio', 'Impuesto de industria y comercio por pagar'),
        ('retenciones_por_pagar', 'Retenciones por pagar'),
        ('retencion_fuente_por_pagar', 'Retención en la fuente por pagar'),
        ('retencion_iva_por_pagar', 'Retención de IVA por pagar'),
    ],
    'Conceptos_Diversos': [
        ('otros_gastos_generales', 'Otros gastos generales'),
        ('otros_ingresos_diversos', 'Otros ingresos diversos'),
    ]
}

ESTADO_EN_CURSO = 'En Curso'
ESTADO_FINALIZADO = 'Finalizado'