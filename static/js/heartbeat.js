
function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}
(function worker() {
  $.ajax({
    url: '/heartbeat',
    data:{'key':getCookie('key')},
    type:'POST',
    success: function(data) {
      console.log(data);
      },
    complete: function() {
      // Schedule the next request when the current one's complete
      setTimeout(worker, 180000);
    }
  });
})();
