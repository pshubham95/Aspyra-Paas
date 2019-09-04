$(function() {
  var getQueryString = function ( field, url ) {
    var href = url ? url : window.location.href;
    var reg = new RegExp( '[?&]' + field + '=([^&#]*)', 'i' );
    var string = reg.exec(href);
    return string ? string[1] : null;
};
  $('#stop').click(function() {
    document.getElementById('b').style.opacity = '0.4';
    document.getElementById('start').disabled = true;
    document.getElementById('del').disabled = true;
    document.getElementById('stop').disabled = true;



    $.ajax({
        url: '/cms_stop',
        data:{'pid':getQueryString('pid')},
        type:'POST',
        success: function(response) {
          document.getElementById('b').style.opacity = '1.0';
          document.getElementById('start').disabled = false;
          document.getElementById('del').disabled = false;
          document.getElementById('stop').disabled = false;

          window.location.href = window.location.href;

        },
        error: function(error) {

          console.log(error);

        }

  });


});

$('#start').click(function() {
  document.getElementById('b').style.opacity = '0.4';
  document.getElementById('start').disabled = true;
  document.getElementById('del').disabled = true;
  document.getElementById('stop').disabled = true;


  $.ajax({
      url: '/cms_start',
      data:{'pid':getQueryString('pid')},
      type:'POST',
      success: function(response) {
        document.getElementById('b').style.opacity = '1.0';
        document.getElementById('start').disabled = false;
        document.getElementById('del').disabled = false;
        document.getElementById('stop').disabled = false;

        window.location.href = window.location.href;

      },
      error: function(error) {

        console.log(error);

      }

});


});

$('#del').click(function() {
  document.getElementById('b').style.opacity = '0.4';
  document.getElementById('start').disabled = true;
  document.getElementById('del').disabled = true;
  document.getElementById('stop').disabled = true;


  $.ajax({
      url: '/cms_delete',
      data:{'pid':getQueryString('pid')},
      type:'POST',
      success: function(response) {
        document.getElementById('b').style.opacity = '1.0';
        document.getElementById('start').disabled = false;
        document.getElementById('del').disabled = false;
        document.getElementById('stop').disabled = false;

        window.location.href = '/login';

      },
      error: function(error) {

        console.log(error);

      }

});


});

});
