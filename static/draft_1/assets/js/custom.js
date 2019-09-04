var page = 1;
function validate()
{
    var name = document.getElementById('container').value;
    
    if ( (name == null || name == "") && page == 1 )
    {
        window.alert('Please fill in the container name');
        document.getElementById('error-1').style.display = 'block';
        
    }
    
    
    else
    {
        document.getElementById('error-1').style.display = 'none';
        
        if(document.getElementById('file_upload').value == ""  && page == 2)
    {
            window.alert('Please upload the executable');
            document.getElementById('error-2').style.display = 'block';
            

    }else
        document.getElementById('error-2').style.display = 'none';

    }
    
    page = page + 1
    
}

function reduce()
{   
    if(page > 1)
    page = page - 1;
}

$(document).ready(function() {
	$("#container").keyup(function (e) {

		//removes spaces from username
		$(this).val($(this).val().replace(/\s/g, ''));

		var container = $(this).val();
		

		if(container.length >= 1){
			$("#user-result").html('<img src="images/available.png" />');
            document.getElementById('next_button').disabled = false;
            document.getElementById('success_1').style.display = 'block';
                        document.getElementById('error_1').style.display = 'none';
            
           





			
		}
        
        else
        {
            $("#user-result").html('<img src="images/not-available.png" />');
            document.getElementById('next_button').disabled = true;
            document.getElementById('error_1').style.display = 'block';
            document.getElementById('success_1').style.display = 'none';

        }
	})
    
    $("#file_upload").change(function (e) {
        var fileName = $(this).val();
        
        if(fileName)
        {
            document.getElementById('next_button').disabled = false;
            document.getElementById('success_2').style.display = 'block';
                        document.getElementById('error_2').style.display = 'none';
            
        }
        
        else
        {
    
            document.getElementById('next_button').disabled = true;
            document.getElementById('error_2').style.display = 'block';
            document.getElementById('success_2').style.display = 'none';
        }
    
    })
});

function Loader()
{
                document.getElementById('next_button').disabled = true;
                document.getElementById('user-result').innerHTML = '<img src="images/not-available.png" />' ;
                localStorage.setItem('page',1);

}

function button_check()
{
    var elem1 = document.getElementById("success_1");
if (elem1.currentStyle) {
    var displayStyle1 = elem1.currentStyle.display;
} else if (window.getComputedStyle) {
    var displayStyle1 = window.getComputedStyle(elem1, null).getPropertyValue("display");
}

var elem2 = document.getElementById("error_1");
if (elem2.currentStyle) {
    var displayStyle2 = elem2.currentStyle.display;
} else if (window.getComputedStyle) {
    var displayStyle2 = window.getComputedStyle(elem2, null).getPropertyValue("display");
}
    
    var elem3 = document.getElementById("success_2");
if (elem3.currentStyle) {
    var displayStyle3 = elem3.currentStyle.display;
} else if (window.getComputedStyle) {
    var displayStyle3 = window.getComputedStyle(elem3, null).getPropertyValue("display");
}
    var elem4 = document.getElementById("error_2");
if (elem4.currentStyle) {
    var displayStyle4 = elem4.currentStyle.display;
} else if (window.getComputedStyle) {
    var displayStyle4 = window.getComputedStyle(elem4, null).getPropertyValue("display");
}
    
    if(displayStyle1 == 'block' || displayStyle3 == 'block')
                        document.getElementById('next_button').disabled = false;
    
    if(displayStyle1 == 'none' || displayStyle3 == 'none')
                        document.getElementById('next_button').disabled = true;
}


$(document).ready(function() {
	$("#next_button").click(function (e) {

		page = parseInt(localStorage.getItem('page'));
        page = page + parseInt(1);
        localStorage.setItem('page',page);
		console.log(page);
        if(page == 4){
        var name = document.getElementById('container').value;
		var softwares = $('#duallist').val();
        softwares = JSON.stringify(softwares);
        var baseos =  document.getElementById('base_os').value;
        var ram =  document.getElementById('ram').value;
        var hd =  document.getElementById('hd').value;
        console.log(name);
        console.log(softwares);
        console.log(baseos);
        console.log(ram);
        console.log(hd);
		document.getElementById('next_button').style.display = 'none';
			$.post('insert_data.php', {'container_name':name,'softwares':softwares,'baseos':baseos,'ram':ram,'hd':hd}, function(data) {
			  
			});
        }
		
	})
    
    $("#prev_button").click(function (e) {
    page = parseInt(localStorage.getItem('page'));
    if ( page > 1)
        page = page - 1
    localStorage.setItem('page',page);
    })
});