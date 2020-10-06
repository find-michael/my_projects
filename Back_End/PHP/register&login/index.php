<?php
	session_start();
	if (isset($_SESSION['logged_in']) && $_SESSION['logged_in'] == true) {
		header('Location: home.php');
		exit();
	}
?>

<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">

	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
	<link href="https://fonts.googleapis.com/css?family=Montserrat&display=swap" rel="stylesheet">
	<link rel="stylesheet" type="text/css" href="Styles/index_style.php">

	<title>PHP</title>
</head>
<body>

<div class="container">
	<div class="left-side">
		<div class="form-login-container">
			<div class="login-title">LOG IN</div>
			<form action="login.php" method="post">
				<div class="form-login form-element">
					<input type="text" name="login-email" id="login-email" class="input-form" placeholder="Email" autocomplete="off" 
					<?php 
						if (isset($_SESSION['login_email'])) {echo 'value="'.$_SESSION['login_email'].'"'; unset($_SESSION['login_email']);}
						if (isset($_SESSION['login_error'])) {echo 'style="border: 1px solid red"';}
					?>>
					<?php 
						if (isset($_SESSION['login_error'])) {
							echo '<div class="input-error">'.$_SESSION['login_error'].'</div>';
							unset($_SESSION['login_error']);}
					?>
				</div>
				<div class="form-password form-element">
					<input type="password" name="login-password" id="login-password" class="input-form" placeholder="Key"
					<?php 
						if (isset($_SESSION['login_pass_error'])) {echo 'style="border: 1px solid red"';}
					?>>
					<?php 
						if (isset($_SESSION['login_pass_error'])) {
							echo '<div class="input-error">'.$_SESSION['login_pass_error'].'</div>'; 
							unset($_SESSION['login_pass_error']);}
					?>
					<div class="show-password">
						<img src="Icons/show-30.png" alt="">
					</div>
				</div>
				<div class="form-login-submit form-element">
					<div class="forgot-password"><a href="#">Forgot your password?</a></div>
					<input type="submit" value="Let me in" id="login-button">
				</div>
			</form>
			<?php 
				if (isset($_SESSION['user_not_found'])) {
					echo '<div class="login-form-fail">'.$_SESSION['user_not_found'].'</div>';
					unset($_SESSION['user_not_found']);}
			?>
		</div>
	</div>
	<div class="right-side">
		<div class="form-reg-container">
			<div class="reg-title">REGISTER</div>
			<form action="register.php" method="post">
				<div class="form-name form-element">
					<input type="text" name="reg-name" id="reg-name" class="input-form" placeholder="Name" autocomplete="off"
					<?php 
						if (empty($_SESSION['reg_success'])) {
							if (isset($_SESSION['reg_name'])) {echo 'value="'.$_SESSION['reg_name'].'"'; unset($_SESSION['reg_name']);}
						} 
						if (isset($_SESSION['reg_name_error'])) {echo 'style="border: 1px solid red"';}
					?>>
					<?php
						if (isset($_SESSION['reg_name_error'])) {
							echo '<div class="input-error">'.$_SESSION['reg_name_error'].'</div>';
							unset($_SESSION['reg_name_error']);}
					?>
				</div>
				<div class="form-s-name form-element">
					<input type="text" name="reg-s-name" id="reg-s-name" class="input-form" placeholder="Second name" autocomplete="off" 
					<?php 
						if (empty($_SESSION['reg_success'])) {
							if (isset($_SESSION['reg_s_name'])) {echo 'value="'.$_SESSION['reg_s_name'].'"'; unset($_SESSION['reg_s_name']);} 
						}
						if (isset($_SESSION['reg_s_name_error'])) {echo 'style="border: 1px solid red"';}
					?>>
					<?php
						if (isset($_SESSION['reg_s_name_error'])) {
							echo '<div class="input-error">'.$_SESSION['reg_s_name_error'].'</div>';
							unset($_SESSION['reg_s_name_error']);}
					?>
				</div>
				<div class="form-email form-element">
					<input type="text" name="reg-email" id="reg-email" class="input-form" placeholder="Email" autocomplete="off" 
					<?php 
						if (empty($_SESSION['reg_success'])) {
							if (isset($_SESSION['reg_email'])) {echo 'value="'.$_SESSION['reg_email'].'"'; unset($_SESSION['reg_email']);} 
						} 
						if (isset($_SESSION['reg_email_error'])) {echo 'style="border: 1px solid red"';}
					?>>
					<?php
						if (isset($_SESSION['reg_email_error'])) {
							echo '<div class="input-error">'.$_SESSION['reg_email_error'].'</div>';
							unset($_SESSION['reg_email_error']);}
					?>
				</div>
				<div class="form-password form-element">
					<input type="password" name="reg-password" id="reg-password" class="input-form" placeholder="Key"
					<?php 
						if (isset($_SESSION['reg_pass_error'])) {echo 'style="border: 1px solid red"';}
					?>>
					<?php
						if (isset($_SESSION['reg_pass_error'])) {
							echo '<div class="input-error">'.$_SESSION['reg_pass_error'].'</div>';
							unset($_SESSION['reg_pass_error']);}
					?>
					<div class="show-password">
						<img src="Icons/show-30.png" alt="">
					</div>
				</div>
				<div class="form-reg-submit form-element">
					<input type="submit" value="Im in" id="reg-button">
				</div>
			</form>
			<?php
			if (isset($_SESSION['email_already_used'])) {
				echo '<div class="reg-form-fail">This email is already used</div>';
				unset($_SESSION['email_already_used']);
			} else if (isset($_SESSION['reg_success'])) {
				echo '<div class="reg-form-success">Successfull registration</div>';
				unset($_SESSION['reg_success']);
			}
			?>
		</div>
	</div>
</div>

<script type="text/javascript" src="Scripts/index_script.js"></script> 
</body>
</html>