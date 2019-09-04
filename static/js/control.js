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
    document.getElementById('sub').disabled = true;



    $.ajax({
        url: '/stop_single_c',
        data:{'name':document.getElementById('app_name').innerHTML},
        type:'POST',
        success: function(response) {
          document.getElementById('b').style.opacity = '1.0';
          document.getElementById('start').disabled = false;
          document.getElementById('del').disabled = false;
          document.getElementById('stop').disabled = false;
          document.getElementById('sub').disabled = false;

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
  document.getElementById('sub').disabled = true;


  $.ajax({
      url: '/start_single_c',
      data:{'name':document.getElementById('app_name').innerHTML},
      type:'POST',
      success: function(response) {
        document.getElementById('b').style.opacity = '1.0';
        document.getElementById('start').disabled = false;
        document.getElementById('del').disabled = false;
        document.getElementById('stop').disabled = false;
        document.getElementById('sub').disabled = false;

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
  document.getElementById('sub').disabled = true;


  $.ajax({
      url: '/del_single_c',
      data:{'name':document.getElementById('app_name').innerHTML,'pid':getQueryString('pid')},
      type:'POST',
      success: function(response) {
        document.getElementById('b').style.opacity = '1.0';
        document.getElementById('start').disabled = false;
        document.getElementById('del').disabled = false;
        document.getElementById('stop').disabled = false;
        document.getElementById('sub').disabled = false;

        window.location.href = '/login';

      },
      error: function(error) {

        console.log(error);

      }

});


});

});
