function change_pic()
{
    document.getElementById('pic').style.display = 'none';
    document.getElementById('edit_pic').style.display = "block";
  document.getElementById('photo_button').disabled = true;
  document.getElementById('photo_button').style.display = 'block';


}

function change_num()
{
    document.getElementById('number').style.display = 'none';
    document.getElementById('num').style.display = 'block';
    document.getElementById('phone_button').style.display = 'block';
     document.getElementById('phone_button').disabled = true;

}

function change_email()
{
    document.getElementById('email').style.display = 'none';
    document.getElementById('e').style.display = 'block';
    document.getElementById('email_button').style.display = 'block';
     document.getElementById('email_button').disabled = true;

}

function check_email()
{
    var email = document.getElementById('em').value;
    var filter=/^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
if (filter.test(email))
{
    document.getElementById('e').className = 'form-group has-success';
            document.getElementById('right1').style.display = '';
            document.getElementById('wrong1').style.display = 'block';
             document.getElementById('error_message2').innerHTML = '';

            document.getElementById('email_button').disabled = false;


}
    
else
{
    document.getElementById('e').className = 'form-group has-error';
            document.getElementById('right1').style.display = '';
            document.getElementById('wrong1').style.display = 'block';
            document.getElementById('error_message2').innerHTML = 'Invalid E-mail address';
  
            document.getElementById('email_button').disabled = true;
}
}
function check_num()
{
    var ph =     document.getElementById('ph').value;
    if(ph.length != 10)
        {
            document.getElementById('num').className = 'form-group has-error';
            document.getElementById('wrong').style.display = '';
            document.getElementById('right').style.display = 'block';
            document.getElementById('error_message1').innerHTML = 'Phone Number should be 10 digits';
            document.getElementById('phone_button').disabled = true;


        }
    else{
        
            document.getElementById('num').className = 'form-group has-success';
            document.getElementById('right').style.display = '';
            document.getElementById('wrong').style.display = 'block';
                
            document.getElementById('phone_button').disabled = false;

                        document.getElementById('error_message1').innerHTML = '';

    }

}

function pic_check()
{
    if(document.getElementById('edit_pic').value != '')
        {
            document.getElementById('photo_button').disabled = false;
        }
}

   