document.addEventListener('DOMContentLoaded', function() {
    // Obtener todos los checkboxes y totales de items
    const checkboxes = document.querySelectorAll('input[name="item_check"]');
    const totalLabel = document.getElementById('totalSeleccionado');
    const totalRestanteLabel = document.getElementById('totalRestante');

    // Obtener el subtotal total desde la plantilla
    const subtotal = parseFloat(document.getElementById('totalRestante').textContent.replace('$', '').trim());

    // Función para actualizar el total seleccionado y el restante
    function updateTotals() {
        let totalSeleccionado = 0;

        // Calcular el total de los items seleccionados
        checkboxes.forEach((checkbox, index) => {
            if (checkbox.checked) {
                const itemTotal = parseFloat(document.querySelectorAll('.item-total')[index].textContent.replace('$', ''));
                totalSeleccionado += itemTotal;
            }
        });

        // Actualizar el total de los items seleccionados
        totalLabel.textContent = totalSeleccionado.toFixed(3);

        // Calcular y actualizar el total restante
        const totalRestante = subtotal - totalSeleccionado;
        totalRestanteLabel.textContent = totalRestante.toFixed(3);
    }

    // Agregar un evento para cada checkbox
    checkboxes.forEach((checkbox) => {
        checkbox.addEventListener('change', updateTotals);
    });
});
