$(function() {
  var getQueryString = function ( field, url ) {
    var href = url ? url : window.location.href;
    var reg = new RegExp( '[?&]' + field + '=([^&#]*)', 'i' );
    var string = reg.exec(href);
    return string ? string[1] : null;
};
var ip = '192.168.2.6'; //change ip here
  $.ajax({
      url: '/getdisk',
      data:{'pid':getQueryString('pid')},
      type: 'POST',


success: function(response) {
  var response = JSON.parse(response);
  document.getElementById('disk').innerHTML = response['size'];
  if(parseInt(response['real']) > 52428800)
  {
    document.getElementById('file_upload').style.display = 'none';
  }
},
error: function(error) {
  console.log(error);

}
});

});
