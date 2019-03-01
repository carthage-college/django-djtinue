$(function() {
    jQuery.support.placeholder = false;
    test = document.createElement('input');
    // inFieldLabels plugin adds placeholder feature similar to html5.
    if('placeholder' in test) jQuery.support.placeholder = true;
    if(!$.support.placeholder) {
        $("label").inFieldLabels();
        $("input").attr("autocomplete","off");
    } else {
        $(".placeholder").hide();
    }

    /* payment options. hide credit card form if not cc. */
    $('#id_payment_type_0').click(function() {
        $('#payment-details').show();
    });
    $('#id_payment_type_1').click(function() {
        $('#payment-details').hide();
    });
    $('#id_payment_type_2').click(function() {
        $('#payment-details').hide();
    });
    $('textarea').trumbowyg({
      btns: [
        ['formatting'], ['strong', 'em', 'del'], ['link'],
        ['justifyLeft', 'justifyCenter', 'justifyRight', 'justifyFull'],
        ['unorderedList', 'orderedList'], ['horizontalRule'], ['viewHTML'],
      ],
      semantic: true, autogrow: true, resetCss: true
    });
    $('form#profile').bind('submit', function (e) {
      // disable submit
      $('form#profile input[type=submit]').prop('disabled', true);
      return true;
    });
});
