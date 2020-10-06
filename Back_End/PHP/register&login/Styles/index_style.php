<?php
    header("Content-type: text/css; charset: UTF-8");
?>



* {
	margin: 0;
	padding: 0;
	font-family: 'Montserrat', sans-serif;
}

@media (max-width: 800px) {
	.container {
		flex-direction: column;
		height: 200vh;
	}
	.left-side, .right-side {
		width: 100%;
	}
}
@media (min-width: 801px) {
	.container {
		height: 100vh;
	}
	.left-side, .right-side {
		width: 50%;
	}
}

.container {
	width: 100%;
	display: flex;
	background-image: radial-gradient( circle farthest-corner at -4% -12.9%,  rgba(74,98,110,1) 0.3%, rgba(30,33,48,1) 90.2% );
	overflow: hidden;
	min-width: 400px;
}

.left-side, .right-side {
	height: 100%;
	display: flex;
	align-items: center;
	justify-content: center;
}

.form-login-container, .form-reg-container {
	position: relative;
	width: 375px;
	box-shadow: 0 8px 6px -6px black;
	border-radius: 10px;
	display: flex;
	align-items: center;
	justify-content: center;
}

.form-login-container {
	height: 400px;
	background-image: linear-gradient( 109.6deg,  rgba(20,30,48,1) 11.2%, rgba(36,59,85,1) 91.1% );
}

.form-reg-container {
	height: 570px;
	background-image: radial-gradient( circle farthest-corner at 10% 20%,  rgba(151,10,130,1) 0%, rgba(33,33,33,1) 100.2% );
}

.form-element {
	margin: 45px;
	position: relative;
}

.input-form {
	position: relative;
	box-sizing: border-box;
	z-index: 2;
	height: 50px;
	width: 320px;
	border-radius: 10px;
	outline: none;
	padding-left: 10px;
	padding-right: 45px;
	box-shadow: 0 8px 6px -6px black;
	font-size: 20px;
	opacity: 0.9;
	border: none;
	transition: opacity .2s ease-in-out;
}

input[type="text"]:focus, input[type="password"]:focus {
	opacity: 1;
}

#login-button, #reg-button {
	height: 40px;
	width: 100%;
	border-radius: 10px;
	border-width: 0;
	outline: none;
	padding-left: 10px;
	padding-right: 10px;
	box-shadow: 0 8px 6px -6px black;
	text-shadow: 2px 4px 3px rgba(0,0,0,0.3);
	cursor: pointer;
	font-size: 20px;
	transition: background-color .2s ease-in-out;
}

#login-button:hover, #reg-button:hover {
	background-color: #eeeeee;
}

.input-error {
	position: absolute;
	z-index: 1;
	color: red;
	padding-top: 8px;
	font-size: 14px;
	text-shadow: 2px 4px 3px rgba(0,0,0,0.3);
	animation: form_empty 0.2s ease-in-out;
}

@keyframes form_empty {
	0% {
		bottom: 0px;
		opacity: 0;
	}
	100% {
		bottom: -27px;
		opacity: 1;
	}
}

.login-form-fail, .reg-form-fail, .reg-form-success {
	position: absolute;
	left: 50%;
	white-space: nowrap;
	transform: translateX(-50%);
	text-shadow: 2px 4px 3px rgba(0,0,0,0.3);
	animation: form_fail 0.2s ease-in-out;
}

.login-form-fail {
	color: red;
	top: 30px;
}

.reg-form-fail {
	color: red;
	top: 20px;
}

.reg-form-success {
	color: lime;
	top: 22px;
}

@keyframes form_fail {
	0% {
		opacity: 0;
	}
	100% {
		opacity: 1;
	}
}

.login-title, .reg-title {
	position: absolute;
	font-size: 30px;
	font-weight: bold;
	color: white;
	opacity: 0.8;
	text-shadow: 2px 4px 3px rgba(0,0,0,0.3);
}

.login-title {
	left: 5px;
	top: -40px;
}

.reg-title {
	bottom: -40px;
	right: 5px;
}

.clear-input, .show-password {
	position: absolute;
	height: 35px;
	width: 35px;
	right: 5px;
	top: 50%;
	border-radius: 50%;
	transform: translateY(-50%);
	background-color: transparent;
	z-index: 3;
	cursor: pointer;
	transition: all .2s ease-in-out;
	display: flex;
	align-items: center;
	justify-content: center;
}

.clear-input:hover, .show-password:hover {
	background-color: lightgrey;
}

.clear-input img, .show-password img {
	width: 50%;
	height: 50%;
	opacity: 0.4;
	transition: opacity .2s ease-in-out;
}

.clear-input:hover img, .show-password:hover img {
	opacity: 1;
}

.forgot-password a {
	text-decoration: none;
	text-shadow: 2px 4px 3px rgba(0,0,0,0.3);
	color: #5c7796;
	font-size: 12px;
}

.forgot-password a:hover {
	text-decoration: underline;
}

.forgot-password {
	margin-bottom: 5px;
}

.form-reg-submit {
	margin-top: 70px;
}
