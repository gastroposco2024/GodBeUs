$(document).ready(function() {
    window.mostrarModal = function() {
        $('#modalPago').show();
    };

    window.cerrarModal = function() {
        $('#modalPago').hide();
    };

    $(window).on('click', function(event) {
        if ($(event.target).is('#modalPago')) {
            $('#modalPago').hide();
        }
    });

    $('#form-modal-crear-pedido').on('submit', function(event) {
        event.preventDefault();

        var formData = $(this).serialize();
        var submitButton = $(this).find('button[type="submit"]');
        submitButton.prop('disabled', true);

        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: formData,
            success: function(response) {
                if (response.redirect_url) {
                    window.location.href = response.redirect_url;
                } else {
                    alert('Pedido creado con éxito.');
                    cerrarModal();
                }
            },
            error: function(xhr, status, error) {
                alert('Error en la solicitud: ' + error);
                submitButton.prop('disabled', false);
            }
        });
    });
});
