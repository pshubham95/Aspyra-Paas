$(function() {
  var getQueryString = function ( field, url ) {
    var href = url ? url : window.location.href;
    var reg = new RegExp( '[?&]' + field + '=([^&#]*)', 'i' );
    var string = reg.exec(href);
    return string ? string[1] : null;
};
var ip = '192.168.2.6'; //change ip here
  $.ajax({
      url: '/getapp_data',
      data:{'pid':getQueryString('pid')},
      type: 'POST',


success: function(response) {
  var response = JSON.parse(response);
  response['port'] = JSON.parse(response['port']);
  if(response['type'] != '1')
  {
    window.location.href = '/error';
  }
  if(response['status'] == 'started')
  {
    document.getElementById('start').disabled = true;
  }
  if(response['status'] == 'stopped')
  {
    document.getElementById('display').style.display = 'none';
  }
  document.getElementById('app_name').innerHTML = response['name'];
  document.getElementById('ip').innerHTML = 'http://'+ip+':'+response['port']['port1'];
  document.getElementById('ip_a').href = 'http://'+ip+':'+response['port']['port1'];

  document.getElementById('tomcat_ip').innerHTML = 'http://'+ip+':'+response['port']['port2'];
  document.getElementById('tomcat_ip_a').href = 'http://'+ip+':'+response['port']['port2'];

  document.getElementById('admin_ip').innerHTML = 'http://'+ip+':'+response['port']['port2']+'/manager/html';
  document.getElementById('admin_ip_a').href = 'http://'+ip+':'+response['port']['port2']+'/manager/html';

  document.getElementById('display').src = 'http://'+ip+':'+response['port']['port1'];
  document.getElementById('display').src = document.getElementById('display').src;

},
error: function(error) {
  window.location.href = '/error';

  console.log(error);

}
});

});
