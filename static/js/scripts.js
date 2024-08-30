// static/js/scripts.js

function eliminarItem(itemId, pedidoId, csrfToken) {
    if (confirm('¿Estás seguro de que quieres eliminar este plato?')) {
        $.ajax({
            url: `/eliminar_item_pedido/${itemId}/`,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                if (response.success) {
                    $('#item-' + itemId).remove();
                    alert('Plato eliminado correctamente');
                    location.reload(); // Recargar la página
                } else {
                    alert('Error al eliminar el item.');
                }
            }
        });
    }
}


$(document).ready(function() {
    window.mostrarModal = function(pedidoId) {
        var modal = document.getElementById("modalPago");
        modal.style.display = "block";
        
        var form = document.getElementById("form-finalizar-compra-" + pedidoId);
        if (form) {
            var mesaId = form.querySelector("input[name='mesaid']").value;
            var totalPedido = form.querySelector("input[name='total_pedido']").value;

            var mesaIdInput = document.getElementById("mesaid");
            var totalPedidoInput = document.getElementById("totalPedido");

            if (mesaIdInput && totalPedidoInput) {
                mesaIdInput.value = mesaId;
                totalPedidoInput.value = totalPedido;
            }
        }
    };

    window.cerrarModal = function() {
        var modal = document.getElementById("modalPago");
        modal.style.display = "none";
    };

    window.onclick = function(event) {
        var modal = document.getElementById("modalPago");
        if (event.target === modal) {
            modal.style.display = "none";
        }
    };

    $('#form-modal-pago').submit(function(event) {
        event.preventDefault();

        var formData = $(this).serialize();

        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: formData,
            success: function(response) {
                if (response.success) {
                    alert(response.message);
                    cerrarModal();
                    location.reload();
                } else {
                    alert('Error: ' + response.error);
                    submitButton.prop('disabled', false);
                }
            },
            error: function(xhr, status, error) {
                alert('Error en la solicitud: ' + error);
                submitButton.prop('disabled', false);
            }
        });
    });
}); 

