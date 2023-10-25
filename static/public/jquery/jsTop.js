$(document).ready(function($) {
    $(document).on('click','#logout', function(){
        $('#mb-signout').show();
    });
    $(document).on('click','.mb-control-close',function(){
        $('#mb-signout').hide();
     });

     top();
     function top(){
        var scrollTop = $(".scrollTop");
        $(window).scroll(function() {
            var topPos = $(this).scrollTop();
            if (topPos > 100) {
              $(scrollTop).css("opacity", "1");

            } else {
              $(scrollTop).css("opacity", "0");
            }
        });
        $(scrollTop).click(function() {
          $('html, body').animate({
            scrollTop: 0
          }, 800);
            return false;
        });
    }
    $('[data-toggle="tooltip"]').tooltip();
    $('.timepicker').timepicker({
        showInput: false,
        showMeridian: false,
        secondStep: 1 ,
        minuteStep: 1
    });
    $('.datepicker').datepicker({
      format: 'dd/mm/yyyy',
      autoclose: true
    });
    $('.js-example-basic-multiple').select2();
        $('.datepicker').datepicker({
          format: 'dd/mm/yyyy',
          autoclose: true
    });
    $('.js-example-basic-single').select2();
});
