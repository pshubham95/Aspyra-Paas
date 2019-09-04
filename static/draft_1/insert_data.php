<?php
###### db ##########
$db_username = 'root';
$db_password = '';
$db_name = 'btech';
$db_host = 'localhost';
if(!isset($_SERVER['HTTP_X_REQUESTED_WITH']) AND strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) != 'xmlhttprequest') {
        die();
    }
    
    //try connect to db
    $dbh = new mysqli('localhost','root','','btech');

    $cname = $_POST['container_name'];
    $soft = $_POST['softwares'];
    $base = $_POST['baseos'];
    $ram = $_POST['ram'];
    $hd = $_POST['hd'];

    $sql="INSERT INTO container_data (name,softwares,baseos,ram,hd) VALUES ('$cname','$soft','$base','$ram','$hd')";
    if($dbh->query($sql) === false) 
  	{
  		trigger_error('Wrong SQL: ' . $sql . ' Error: ' . $dbh->error, E_USER_ERROR);
	}
  	
   	$dbh = null;
?>