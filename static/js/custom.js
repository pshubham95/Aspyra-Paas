var c_mis = false;
var c_name = false;
var c_email  = false;
var c_pass = false;
var c_phone = false;
var c_mis_login = false;
var c_pass_login = false;
var r = 0;
function makeid()
{
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < 5; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}

function rem()
{
	if(document.getElementById('r').checked)
	{
		r = 1;	
	}
	
	else
	{
	 	r = 0;	
	}
}
function init()
{
    document.getElementById('btnSignUp').disabled = true;
    document.getElementById('btnSignIn').disabled = true;
    document.getElementById('username').value = "";
    document.getElementById('firstname').value = "";
    document.getElementById('alert-1').style.display = "none";
    
   
    document.getElementById('passwd').value = "";
    document.getElementById('re-passwd').value = "";
    document.getElementById('email').value = "";
    document.getElementById('number').value = "";
	
	
	
	
}

function validate()
{
	if( c_email && c_mis && c_name && c_pass && c_phone)
        {
            document.getElementById('btnSignUp').disabled = false;
        }
    else
    document.getElementById('btnSignUp').disabled = true;

    if(c_mis_login && c_pass_login)
    document.getElementById('btnSignIn').disabled = false;
    else
    document.getElementById('btnSignIn').disabled = true;
   

}
function check_login_mis()
{
    var mis = document.getElementById('login-username').value;
    if(mis == "" || !/\S/.test(mis) )
        {
            c_mis_login = false;
            validate();
        }
    else
        {
            c_mis_login = true;
            validate();
        }
}

function check_login_pass()
{
    var pass = document.getElementById('login-password').value;
	    var mis = document.getElementById('login-username').value;

    if(pass == "" || !/\S/.test(mis) )
        {
            c_pass_login = false;
            validate();
        }
    else
        {
            c_pass_login = true;
            validate();
        }
}



function check_mis()
{
    
    var mis = document.getElementById('username').value;
    if(/^\d+$/.test(mis) && mis.length == 9) {
        c_mis = true;
        document.getElementById('mis').className = "input-group m-b has-success";
            validate();

 //proceed with rest of code
}
    
    else
        {
            document.getElementById('mis').className = "input-group m-b has-error";
            c_mis = false;
            validate();
        }
}

function check_name()
{
    var n = document.getElementById('firstname').value;
    if(!/\S/.test(n) || name == null)
    {
        document.getElementById('fname').className = "input-group m-b has-error";
        c_name = false;
        validate();
    }
    else
    {
    document.getElementById('fname').className = "input-group m-b has-success";
    c_name = true;
            validate();

    }

}

function check_pass()
{
    var pass = document.getElementById('passwd').value;
    var re_pass = document.getElementById('re-passwd').value;
    
    if(!/\S/.test(pass) || !/\S/.test(re_pass) || pass != re_pass || pass.length < 6 || re_pass.length < 6)
    {
        document.getElementById('repass').className =  "input-group m-b has-error";
        document.getElementById('pass').className = "input-group m-b has-error";
        c_pass = false;
        validate();

    }
    
    else
        {
        document.getElementById('repass').className =  "input-group m-b has-success";
        document.getElementById('pass').className =  "input-group m-b has-success";
        c_pass = true;
     validate();

        }
    
}

function check_email()
{
    var email = document.getElementById('email').value;
var filter=/^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
if (filter.test(email))
{
    document.getElementById('mail').className =  "input-group m-b has-success";
    c_email = true;
        validate();

}
    
else
    { 
        document.getElementById('mail').className = "input-group m-b has-error";
        c_email = false;
        validate();

    }
}

function check_phone()
{
    var phone = document.getElementById('number').value;
    if(/^\d+$/.test(phone) && phone.length == 10 ){
            document.getElementById('num').className =  "input-group m-b has-success";
            c_phone = true;
            validate();


    }
    
    else{
        document.getElementById('num').className =  "input-group m-b has-error";
        c_phone = false;
        validate();
    }

}


function clearphoto()
{
    var oldInput = document.getElementById('ph');
    var newInput = document.createElement("input"); 
    newInput.type = "file"; 
    newInput.id = oldInput.id; 
    newInput.name = oldInput.name; 
    newInput.className = oldInput.className; 
    newInput.style.cssText = oldInput.style.cssText; 
    // TODO: copy any other relevant attributes 

    oldInput.parentNode.replaceChild(newInput, oldInput); 
    
    var oldInput = document.getElementById('ph_name');
    var newInput = document.createElement("input"); 
    newInput.type = "file"; 
    newInput.id = oldInput.id; 
    newInput.name = oldInput.name; 
    newInput.className = oldInput.className; 
    newInput.style.cssText = oldInput.style.cssText; 
    // TODO: copy any other relevant attributes 

    oldInput.parentNode.replaceChild(newInput, oldInput); 
}



function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}


$(function() {
	$.ajax({
		
		url: '/checksession',
		type: 'POST',
		data: {'key':getCookie('key')},
		success: function(response) {
			var response = JSON.parse(response);
			if(response['status'] == '200')
			{
				if(document.getElementById('r').checked)
				{
					
				}
				window.location.href = '/login';
			}
			
			else
			{
				document.getElementById('b').style.display = '';
				
			}
			
		},
		
		error: function(error) {
			console.log(error);
			
		}
		
		
	});
    $('#btnSignIn').click(function() {
        $.ajax({
            url: '/getkey',
            type: 'POST',
            success: function(response) {
                var response = JSON.parse(response)
                key = response['key'];
                 $.ajax({
            url: '/signIn',
            data: {'username':document.getElementById('login-username').value,'password':document.getElementById('login-password').value,'r':r},
            type: 'POST',
            success: function(response) {
                var response = JSON.parse(response);
                if(response['status'] == "200")
                {
                    if(document.getElementById('r').checked)
					{
						var hash1 = CryptoJS.AES.encrypt(document.getElementById('login-username').value, getCookie('key'));
						var hash2 = CryptoJS.AES.encrypt(document.getElementById('login-password').value, getCookie('key'));
						localStorage.setItem('u',hash1);
						localStorage.setItem('p',hash2);
						document.cookie = "u="+hash1;
						document.cookie = "p="+hash2;
		

					}
                 
					
                    window.location.href = "/login";
                    
                }
                else
				{
                    document.getElementById('messages').innerHTML = response['status'];
					document.getElementById('s_spin').style.display = 'none';
				}
            },
            error: function(error) {
                console.log(error);
            }
        });
                
            },
            error: function(error) {
                console.log(error);
            }
        });
 
       
    });
});




    
    
/*window.onload = function () {
    if (! localStorage.justOnce) {
        localStorage.setItem("justOnce", "true");
        window.location.reload();
    }
}
*/
$(function() {
    $('#btnSignUp').click(function() {
       var photo = false;
        var signup = false;
        var e = '';
        
document.getElementById('btnSignUp').disabled = true;

        $.ajax({
            url: '/SignUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                
                if(document.getElementById('ph').value){
            var form = $('#photoform')[0]; // You need to use standart javascript object here
        var form_data = new FormData(form);
        form_data.append('mis',document.getElementById('username').value);
        $.ajax({
            type: 'POST',
            url: '/photo',
            data: form_data,
            contentType: false,
            processData: false,
            success: function(response) {
            document.getElementById('content').style.display = 'none';
		    document.getElementById('content2').style.display = 'none';

            document.getElementById('alert-1').style.display = 'block';
            document.getElementById('alert-2').style.display = 'none';
            },
            
            error: function(error) {
                document.getElementById('content').style.display = 'none';
			document.getElementById('content2').style.display = 'none';

            document.getElementById('alert-2').style.display = 'block';
            document.getElementById('alert-1').style.display = 'none';
                
            }
        });
        
        }
            else{
            document.getElementById('content').style.display = 'none';
		    document.getElementById('content2').style.display = 'none';

            document.getElementById('alert-1').style.display = 'block';
            document.getElementById('alert-2').style.display = 'none';
            }
            },
            error: function(error) {
            document.getElementById('content').style.display = 'none';
			document.getElementById('content2').style.display = 'none';

            document.getElementById('alert-2').style.display = 'block';
            document.getElementById('alert-1').style.display = 'none';
            console.log(error);
            }
        });
        
        

        
        
        
        
        
        
        
    });
});

$(function() {
	
	if(localStorage.getItem('u') === null && localStorage.getItem('p') === null)
	{
			

	}
	else
	{
	var decrypted = CryptoJS.AES.decrypt(localStorage.getItem('u'), getCookie('key'));
	var username = decrypted.toString(CryptoJS.enc.Utf8);
	var p = CryptoJS.AES.decrypt(localStorage.getItem('p'), getCookie('key'));
	p = p.toString(CryptoJS.enc.Utf8);
	

	document.getElementById('login-username').value = username;
	document.getElementById('login-password').value = p;
	console.log(username);
	$('#btnSignIn').click();

	}
	
	
    $('#mis').keyup(function() {
       
        var mis = document.getElementById('username').value;
		if(mis.length == 9){
		document.getElementById('proc').style = ''; 
				document.getElementById('na').style.display = 'none'; 
				document.getElementById('avail').style.display = 'none'; 
        $.ajax({
            url: '/checkusername',
            data: "mis="+mis,
            type: 'POST',
            success: function(response) {
				
                var response = JSON.parse(response);
				


                if(response['status'] == 'available' && mis.length == 9 && /^\d+$/.test(mis))
                    {
						document.getElementById('proc').style.display = 'none'; 

                        document.getElementById('avail').style = ''; 
                        document.getElementById('na').style.display = 'none'; 

                        c_mis = true;
                        document.getElementById('mis').className = "input-group m-b has-success";
                        validate();
                    }
                else{
						document.getElementById('proc').style.display = 'none'; 

                        document.getElementById('na').style = '';
                        document.getElementById('avail').style.display = 'none'; 

                        c_mis = false;
                        document.getElementById('mis').className = "input-group m-b has-error";
                        validate();

                    
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
		}
		
		else{
                        document.getElementById('na').style = '';
                        document.getElementById('avail').style.display = 'none'; 

                        c_mis = false;
                        document.getElementById('mis').className = "input-group m-b has-error";
                        validate();

                    
                }
        
        
    });
});


        
    
    

$(document).on('click', '#close-preview', function(){ 
    $('.image-preview').popover('hide');
    // Hover befor close the preview
    $('.image-preview').hover(
        function () {
           $('.image-preview').popover('show');
        }, 
         function () {
           $('.image-preview').popover('hide');
        }
    );    
});

$(function() {
    // Create the close button
    var closebtn = $('<button/>', {
        type:"button",
        text: 'x',
        id: 'close-preview',
        style: 'font-size: initial;',
    });
    closebtn.attr("class","close pull-right");
    // Set the popover default content
    $('.image-preview').popover({
        trigger:'manual',
        html:true,
        title: "<strong>Preview</strong>"+$(closebtn)[0].outerHTML,
        content: "There's no image",
        placement:'bottom'
    });
    // Clear event
    $('.image-preview-clear').click(function(){
        $('.image-preview').attr("data-content","").popover('hide');
        $('.image-preview-filename').val("");
        $('.image-preview-clear').hide();
        $('.image-preview-input input:file').val("");
        $(".image-preview-input-title").text("Browse"); 
    }); 
    // Create the preview image
    $(".image-preview-input input:file").change(function (){     
        var img = $('<img/>', {
            id: 'dynamic',
            width:250,
            height:200
        });      
        var file = this.files[0];
        var reader = new FileReader();
        // Set preview image into the popover data-content
        reader.onload = function (e) {
            $(".image-preview-input-title").text("Change");
            $(".image-preview-clear").show();
            $(".image-preview-filename").val(file.name);            
            img.attr('src', e.target.result);
            $(".image-preview").attr("data-content",$(img)[0].outerHTML).popover("show");
        }        
        reader.readAsDataURL(file);
    });  
});