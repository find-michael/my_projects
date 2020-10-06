<?php
	session_start();
	if (is_null($_SESSION["logged_in"])) {
		header("Location: index.php");
		exit();
	}
?>

<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">

	<link href="https://fonts.googleapis.com/css?family=Montserrat&display=swap" rel="stylesheet">
	<link rel="stylesheet" type="text/css" href="Styles/home_style.css">
	
	<title>Me</title>
</head>
<body>

<div class="container">
	<div class="content">
		<div class="hello">Hello <?php echo $_SESSION['login-email']; ?></div>
		<div class="logout">
			<a href="logout.php">Logout</a>
		</div>
	</div>
</div>
	
</body>
</html>
