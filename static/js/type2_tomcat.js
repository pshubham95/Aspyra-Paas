$(function() {
  var getQueryString = function ( field, url ) {
    var href = url ? url : window.location.href;
    var reg = new RegExp( '[?&]' + field + '=([^&#]*)', 'i' );
    var string = reg.exec(href);
    return string ? string[1] : null;
};
var ip = '10.100.104.143'; //change ip here
  $.ajax({
      url: '/getapp_data',
      data:{'pid':getQueryString('pid')},
      type: 'POST',


success: function(response) {
  var response = JSON.parse(response);
  response['port'] = JSON.parse(response['port']);
  if(response['type'] != '2')
  {
    window.location.href = '/error';
  }
  document.getElementById('app_name').innerHTML = response['name'];
  document.getElementById('ip').innerHTML = 'http://'+ip+':'+response['port']['port1'];
  document.getElementById('ip_a').href = 'http://'+ip+':'+response['port']['port1'];
  document.getElementById('manager_ip').innerHTML = 'http://'+ip+':'+response['port']['port1']+'/manager/';
  document.getElementById('manager_ip_a').href = 'http://'+ip+':'+response['port']['port1']+'/manager/';
  document.getElementById('display').src = 'http://'+ip+':'+response['port']['port1'];
  document.getElementById('display').src = document.getElementById('display').src;

},
error: function(error) {
  window.location.href = '/error';

  console.log(error);

}
});

});
