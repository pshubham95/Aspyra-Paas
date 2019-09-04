function check()
{
   var f_name =  document.getElementById('first_name').value;
console.log(f_name);
   var l_name = document.getElementById('last_name').value;
   var password = document.getElementById('password').value;
   var pass_conf = document.getElementById('password_confirmation').value;
    if(!isNaN(f_name))
    {
        alert('Enter appropriate First Name');
        document.getElementById('first_name').focus;
        return false;
    }
    
    if(!isNaN(l_name))
    {
        alert('Enter appropriate Last Name');
        document.getElementById('last_name').focus;
        return false;
    }
    
    if(password.localeCompare(pass_conf) != 0)
    {
        alert('Passwords do not match');
        document.getElementById('password').focus;
        document.getElementById('password_confirmation').focus;
        return false;
    }
    
    if(document.getElementById('phone').value.length > 10 || document.getElementById('phone').value.length < 8)
    {
        alert('Enter a valid phone number');
        document.getElementById('phone').focus;
        return false;
    }
    return true;
    
    
}


