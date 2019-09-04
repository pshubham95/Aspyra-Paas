var c_name = false;
var c_soft = false;
function check_c_name()
{
    var name = document.getElementById('container-name').value;
    if(name.length > 4)
        {
            c_name = true;
            document.getElementById('container_name').className = 'form-group has-success'
            document.getElementById('right').style = "";
            document.getElementById('wrong').style.display = "none";
            document.getElementById('error_message1').innerHTML = "";

            validate();
        }
    else
        {
            c_name = false;
            document.getElementById('container_name').className = 'form-group has-error'
            document.getElementById('wrong').style = "";
            document.getElementById('right').style.display = "none";
            document.getElementById('error_message1').innerHTML = "Container name should be atleast four letters"
            validate();
        }
}

function getSelectValues(select) {
  var result = [];
  var options = select && select.options;
  var opt;

  for (var i=0, iLen=options.length; i<iLen; i++) {
    opt = options[i];

    if (opt.selected) {
      result.push(opt.value || opt.text);
    }
  }

    if(result.length == 0)
        {
            document.getElementById('soft').className = "form-group has-error";
            c_soft = false;
            validate();
        }
    else
        {
            document.getElementById('soft').className = "form-group has-success";
            c_soft = true;
            validate();
 
        }
}

function validate()
{
    if(c_soft && c_name)
        {
            document.getElementById('next_button').disabled = false;
        }
    else
        {
            document.getElementById('next_button').disabled = true;
 
        }
}

function init()
{   
                document.getElementById('next_button').disabled = true;

}