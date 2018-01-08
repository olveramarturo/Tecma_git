/*
 Deshabilitar el boton de input cuando se realiza un submit
 Previene errores por el dobleclick
*/
$('.btndisable').on('submit', function() {

    console.log('Enviado');
    
    // Creando un contenedor con el documento
    var self = $(this),
	button = self.find('input[type="submit"], button');
    button.attr('disabled', 'disabled').val('Enviando');
        
});
