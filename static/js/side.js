$(function() {
var ip = '192.168.2.6';
  $.ajax({
      url: '/gettable_data',
      type: 'POST',


success: function(response) {
  var response = JSON.parse(response);
  for(var i = 0; i < response.length;i++)
  {
    var port = JSON.parse(response[i][4]);
    document.getElementById('side').innerHTML += '<li ><a href="'+response[i][7]+'?pid='+response[i][1]+'" class="auto"><i class="i i-dot"></i><span>'+response[i][2]+'</span></a></li>'
  }
},
error: function(error) {
  console.log(error);

}
});


});
