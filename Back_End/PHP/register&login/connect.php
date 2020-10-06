<?php 

	$host = "localhost";
	$db_login = "root";
	$db_password = "";
	$db_name = "my_website";

	$connection = @new mysqli($host, $db_login, $db_password, $db_name);
	if ($connection->connect_errno!=0) {
		$connection->close();
		die("Sorry, we are having some problems.");
	}
?>