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
    $('textarea').trumbowyg({
      btns: [
        ['formatting'], ['strong', 'em', 'del'], ['link'],
        ['justifyLeft', 'justifyCenter', 'justifyRight', 'justifyFull'],
        ['unorderedList', 'orderedList'], ['horizontalRule'], ['viewHTML'],
      ],
      tagsToRemove: ['script', 'link'],
      removeformatPasted: true, semantic: true, autogrow: true, resetCss: true
    });
    $('#id_payment_method_0').click(function() {
      $('#creditcard-details').slideDown(200);
      $('#payment-total').slideDown(200)
      $('#payment-waiver').slideUp(200)
    });
    $('#id_payment_method_1').click(function() {
      $('#creditcard-details').slideUp(200);
      $('#payment-total').slideDown(200)
      $('#payment-waiver').slideUp(200)
    });
    $('#id_payment_method_2').click(function() {
      $('#creditcard-details').slideUp(200);
      $('#payment-total').slideDown(200)
      $('#payment-waiver').slideUp(200)
    });
    $('#id_payment_method_3').click(function() {
      $('#creditcard-details').slideUp(200);
      $('#payment-total').slideUp(200)
      $('#payment-waiver').slideDown(200)
    });
    $('#id_total').attr('readonly', true);
    $('form#profile').bind('submit', function (e) {
      // disable submit
      $('form#profile input[type=submit]').prop('disabled', true);
      return true;
    });
});
