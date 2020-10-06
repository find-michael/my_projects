<?php
	
	session_start();

	$name = $_POST['reg-name'];
	$s_name = $_POST['reg-s-name'];
	$email = $_POST['reg-email'];
	$password = $_POST['reg-password'];
	$_SESSION['reg_name'] = $name;
	$_SESSION['reg_s_name'] = $s_name;
	$_SESSION['reg_email'] = $email;

	$email = htmlentities($email, ENT_QUOTES, "UTF-8");
	$password = htmlentities($password, ENT_QUOTES, "UTF-8");

	// INPUT VALIDATION // INPUT VALIDATION // INPUT VALIDATION // INPUT VALIDATION // INPUT VALIDATION // INPUT VALIDATION // INPUT VALIDATION

	$inp_err = false;
	if ($name == '') {
		$_SESSION['reg_name_error'] = 'Type your name'; 
		$inp_err = true;
	} else {
		if (!preg_match("/^[a-zA-Z]*$/",$name)) {
		  	$_SESSION['reg_name_error'] = 'Only letters are allowed';
		  	$inp_err = true;
		} else {
			if (strlen($name) < 2 || strlen($name) > 20) {
				$_SESSION['reg_name_error'] = 'At least 2 to 20 characters is needed'; 
				$inp_err = true;
			}
		}
	}
	if ($s_name == '') {
		$_SESSION['reg_s_name_error'] = 'Type your second name'; 
		$inp_err = true;
	} else {
		if (!preg_match("/^[a-zA-Z]*$/",$s_name)) {
		  	$_SESSION['reg_s_name_error'] = 'Only letters are allowed';
		  	$inp_err = true;
		} else {
			if (strlen($s_name) < 2 || strlen($s_name) > 20) {
				$_SESSION['reg_s_name_error'] = 'At least 2 to 20 characters is needed'; 
				$inp_err = true;
			}
		}
	}
	if ($email == '') {
		$_SESSION['reg_email_error'] = 'Type your email'; 
		$inp_err = true;
	} else {
		if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
		  	$_SESSION['reg_email_error'] = 'Invalid email format';
		  	$inp_err = true;
		} else {
			if (strlen($email) > 30) {
				$_SESSION['reg_email_error'] = 'Email can be up to 30 characters long'; 
				$inp_err = true;
			}
		}
	}
	if ($password == '') {
		$_SESSION['reg_pass_error'] = 'Insert your key'; 
		$inp_err = true;
	} else {
		if (strlen($password) < 5 || strlen($password) > 30) {
			$_SESSION['reg_pass_error'] = 'At least 5 to 30 characters is needed'; 
			$inp_err = true;
		}
	}

	if ($inp_err == true) {
		$inp_err = false;
		header('Location: index.php');
		exit();
	}

	// START INTERACTING WITH DATABASE // START INTERACTING WITH DATABASE // START INTERACTING WITH DATABASE // START INTERACTING WITH DATABASE

	require_once "connect.php";

	$password_hash = password_hash($password, PASSWORD_DEFAULT);

	if ($query_working = @$connection->query(
		sprintf("SELECT * FROM users_data WHERE user_email = '%s'",
		mysqli_real_escape_string($connection, $email),
		))) {
		$result = $query_working->num_rows;
		if ($result < 1) {
			$sql_reg_insert = "INSERT INTO users_data (user_email, user_password, user_name, user_second_name) VALUES ('$email','$password_hash','$name','$s_name')";
			if ($query_working = @$connection->query($sql_reg_insert)) {
				$_SESSION['reg_success'] = true;
				unset($_SESSION['reg_name']);
				unset($_SESSION['reg_s_name']);
				unset($_SESSION['reg_email']);
				$connection->close();
				header('Location: index.php');
				exit();
			} else {
				$connection->close();
				die("Sorry, we are having some problems.");
			}
		} else {
			$_SESSION['email_already_used'] = true;
			header('Location: index.php');
		}
	} else {
		$connection->close();
		die("Sorry, we are having some problems.");
	}
?>