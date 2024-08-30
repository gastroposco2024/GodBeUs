document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('crear-pedido-form');
    var isSubmitting = false;  // Añadir una bandera para controlar el envío

    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();

            if (isSubmitting) {
                return;  // Si el formulario ya se está enviando, salir
            }

            isSubmitting = true;  // Marcar que el formulario se está enviando

            var formData = new FormData(form);

            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': form.querySelector('input[name="csrfmiddlewaretoken"]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                isSubmitting = false;  // Restablecer la bandera

                if (data.redirect_url) {
                    openModal(data.redirect_url);
                } else if (data.message) {
                    showAlert(data.message, data.type);
                } else {
                    console.error('Error al crear el pedido:', data);
                }
            })
            .catch(error => {
                isSubmitting = false;  // Restablecer la bandera en caso de error
                console.error('Error:', error);
            });
        });
    } else {
        console.error('No se encontró el formulario con id="crear-pedido-form"');
    }

    function openModal(url) {
        var iframe = document.getElementById('modalIframe');
        iframe.src = url;

        var modal = new bootstrap.Modal(document.getElementById('pedidoModal'));
        modal.show();
    }

});
