<?php
	
	session_start();

	$login = $_POST['login-email'];
	$password = $_POST['login-password'];
	$_SESSION['login_email'] = $login;

	// INPUT VALIDATION // INPUT VALIDATION // INPUT VALIDATION // INPUT VALIDATION // INPUT VALIDATION // INPUT VALIDATION // INPUT VALIDATION

	$login = htmlentities($login, ENT_QUOTES, "UTF-8");

	$inp_err = false;

	if ($login == '') {
		$_SESSION['login_error'] = 'Insert your email';
		$inp_err = true;
	} else {
		if (!filter_var($login, FILTER_VALIDATE_EMAIL)) {
		  	$_SESSION['login_error'] = 'Invalid email format';
		  	$inp_err = true;
		}
	}
	if ($password == '') {
		$_SESSION['login_pass_error'] = 'Insert your key';
		$inp_err = true;
	}

	if ($inp_err == true) {
		$inp_err = false;
		header('Location: index.php');
		exit();
	}

	// START INTERACTING WITH DATABASE // START INTERACTING WITH DATABASE // START INTERACTING WITH DATABASE // START INTERACTING WITH DATABASE

	require_once "connect.php";

	if ($query_working = @$connection->query(
		sprintf("SELECT * FROM users_data WHERE user_email = '%s'",
		mysqli_real_escape_string($connection, $login)))) {
		$result = $query_working->num_rows;
		if ($result > 0) {
			$data_row = $query_working->fetch_assoc();
			if (password_verify($password, $data_row['user_password'])) {
				$_SESSION['logged_in'] = true;
				header('Location: home.php');
			} else {
				// sleep(5);
				$_SESSION['user_not_found'] = 'Your combination is wrong. Try again';
				header('Location: index.php');
			}
		} else {
			$_SESSION['user_not_found'] = 'Your combination is wrong. Try again';
			header('Location: index.php');
		}
	} else {
		$connection->close();
		die("Sorry, we are having some problems.");
	}
	$connection->close();
?>