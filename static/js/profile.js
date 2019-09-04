function profile(response)
{
    if(response['url'] != '' && response['url'] != ' ')
    {
    document.getElementById('profile').src = response['url']+'_48.png';
	    document.getElementById('profile1').src = response['url']+'_48.png';
    document.getElementById('profile2').src = response['url']+'_48.png';

    }
    document.getElementById('name').innerHTML = response['name'];
	document.getElementById('name1').innerHTML = response['name'];
	document.getElementById('name2').innerHTML = response['name'];
	document.getElementById('loading').style.display = 'none';
	document.getElementById('b').style.opacity = '1.0';




}

function profile_page()
{
  $(document).ready(function(){

          console.log(getCookie('key'));
          $.ajax({
              url: '/getuser_data',
              type: 'POST',
              data:{'key':getCookie('key')},
              success: function(response) {
                  var response = JSON.parse(response);
  				r = response;
          if(response['url'] != '' && response['url'] != ' '){
          document.getElementById('profile3').src = r['url']+'.png';}
          document.getElementById('e').innerHTML = r['email'];
          document.getElementById('m').innerHTML = r['mis'];
          document.getElementById('ph').innerHTML = r['number'];

              },
              error: function(error) {
                  console.log(error);
              }
          });
  });






}

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

$(document).ready(function(){

        console.log(getCookie('key'));
        $.ajax({
            url: '/getuser_data',
            type: 'POST',
            data:{'key':getCookie('key')},
            success: function(response) {
                var response = JSON.parse(response);
				r = response;
                profile(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
});
