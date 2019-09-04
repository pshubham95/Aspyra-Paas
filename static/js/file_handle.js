$(function(){

$('#sub').click(function() {

  document.getElementById('b').style.opacity = '0.4';
  document.getElementById('sub').disabled = true;



var form = $('#upexec')[0]; // You need to use standart javascript object here
    var form_data = new FormData(form);
var app_n = document.getElementById('app_name').innerHTML;
form_data.append('name',app_n);
    $.ajax({
        url: '/file_handle_deploy',
  data:form_data,
        type: 'POST',
  processData: false,
  contentType: false,


        success: function(response) {
          document.getElementById('sub').disabled = false;
          document.getElementById('b').style.opacity = '1.0';
          var response = JSON.parse(response);
          if(response['status'] == 'success')
          {
            window.location.href = window.location.href;
          }

          if(response['status'] == 'error')
          {
            window.location.href = '/deploy_test_err'
          }
  },

  error: function(error) {
    console.log(error);

  }

});
});

});
