document.addEventListener('DOMContentLoaded', function () {
    // Obtener los datos JSON de los elementos script
    var platosNombres = JSON.parse(document.getElementById('platosNombres').textContent);
    var platosNombresDomicilio = JSON.parse(document.getElementById('platosNombresDomicilio').textContent);
    var platosCantidades = JSON.parse(document.getElementById('platosCantidades').textContent);
    var platosCantidadesDomicilio = JSON.parse(document.getElementById('platosCantidadesDomicilio').textContent);
    var tiposPago = JSON.parse(document.getElementById('tiposPago').textContent);
    var ventasTiposPago = JSON.parse(document.getElementById('ventasTiposPago').textContent);
    var meses = JSON.parse(document.getElementById('meses').textContent);
    var ventas_meses = JSON.parse(document.getElementById('ventas_meses').textContent);
    var ventas_meses_domicilio = JSON.parse(document.getElementById('ventas_meses_domicilio').textContent);

    // Gráfico de Platos Más Vendidos
    var ctxPlatos = document.getElementById('platosMasVendidosChart').getContext('2d');
    new Chart(ctxPlatos, {
        type: 'bar',
        data: {
            labels: platosNombres,
            datasets: [{
                label: 'Cantidad Vendida',
                data: platosCantidades,
                backgroundColor: 'rgba(196, 74, 35, 1)',
                borderColor: 'rgba(50, 206, 86, 1)',
                borderWidth: 1
            },
            {
                type: 'line', // Tipo de gráfico para este conjunto de datos
                label: 'Cantidad',
                data: platosCantidades,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    var ctxPlatos = document.getElementById('platosMasVendidosDomicilioChart').getContext('2d');
    new Chart(ctxPlatos, {
        type: 'bar',
        data: {
            labels: platosNombresDomicilio,
            datasets: [{
                label: 'Cantidad Vendida',
                data: platosCantidadesDomicilio,
                backgroundColor: 'rgba(196, 162, 35, 1)',
                borderColor: 'rgba(50, 206, 86, 1)',
                borderWidth: 1
            },
            {
                type: 'line', // Tipo de gráfico para este conjunto de datos
                label: 'Cantidad',
                data: platosCantidadesDomicilio,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });


    // Gráfico de Ventas por Tipo de Pago
var ctxTiposPago = document.getElementById('ventasTipoPagoChart').getContext('2d');
new Chart(ctxTiposPago, {
    type: 'pie',
    data: {
        labels: tiposPago,
        datasets: [{
            label: 'Ventas por Tipo de Pago',
            data: ventasTiposPago,
            backgroundColor: [
                'rgba(255, 0, 0, 0.6)',   // Rojo
                'rgba(255, 127, 0, 0.6)', // Naranja
                'rgba(255, 255, 0, 0.6)', // Amarillo
                'rgba(0, 255, 0, 0.6)',   // Verde
                'rgba(0, 0, 255, 0.6)',   // Azul
                'rgba(75, 0, 130, 0.6)'   // Índigo
                // Puedes agregar más colores del arcoíris si es necesario
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
    }
});

    // Gráfica para Ventas por Mes
    var ctxVentasMes = document.getElementById('ventasMesChart').getContext('2d');
    new Chart(ctxVentasMes, {
        type: 'bar', // Tipo principal del gráfico
        data: {
            labels: meses,
            datasets: [
                {
                    type: 'line', // Tipo de gráfico para este conjunto de datos
                    label: 'Ventas por Mes (Línea)',
                    data: ventas_meses,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    fill: false
                },
                {
                    type: 'bar', // Tipo de gráfico para este conjunto de datos
                    label: 'Ventas por Mes (Barras)',
                    data: ventas_meses,
                    backgroundColor: 'rgba(28, 34, 154, 1)',
                    borderColor: 'rgba(255, 159, 64, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        color: 'white' // Cambia el color de las etiquetas de la leyenda a blanco
                    }
                },
                tooltip: {
                    callbacks: {
                        labelTextColor: function() {
                            return '#fff'; // Cambia el color del texto del tooltip a blanco
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    // Gráfica para Ventas por Mes
    var ctxVentasMes = document.getElementById('ventasMesDomicilioChart').getContext('2d');
    new Chart(ctxVentasMes, {
        type: 'bar', // Tipo principal del gráfico
        data: {
            labels: meses,
            datasets: [
                {
                    type: 'line', // Tipo de gráfico para este conjunto de datos
                    label: 'Ventas por Mes (Línea)',
                    data: ventas_meses_domicilio,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    fill: false
                },
                {
                    type: 'bar', // Tipo de gráfico para este conjunto de datos
                    label: 'Ventas por Mes (Barras)',
                    data: ventas_meses_domicilio,
                    backgroundColor: 'rgba(28, 150, 184, 1)',
                    borderColor: 'rgba(255, 159, 64, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        color: 'white' // Cambia el color de las etiquetas de la leyenda a blanco
                    }
                },
                tooltip: {
                    callbacks: {
                        labelTextColor: function() {
                            return '#fff'; // Cambia el color del texto del tooltip a blanco
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
