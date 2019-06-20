<!DOCTYPE html>
<html>
<head>
		<link rel="stylesheet" href="styles.css" />
		<meta name="viewport"
					content="width=device-width, initial-scale=1"
					charset="UTF-8">
		<title>Devnull's Robotic Car</title>
</head>
<body>
	<div class="topnav">
		<a href="index.html">Home</a>
		<a href="startpi.php">PiCar</a>
		<a class="active" href="downloads.php">Downloads</a>
		<a href="joystick.html">Joystick Testing</a>
		<a href="#contact">Contact</a>
		<a href="#about">About</a>
	</div>
	<h1> Download project files </h1>
	<p>
		<h3>Clone from github</h3>
		<label for="https">https</label>
		<input type="text"
			class="form-control input-monospace input-sm"
			data-autoselect value="git clone https://github.com/jerome1232/PiCar.git"
			aria-label="Clone this repo at git@github.com: jerome1232/PiCar.git"
			readonly size="43" id="https"><br>
		<label for="ssh">ssh</label>
		<input type="text"
		class="form-control input-monospace input-sm"
		data-autoselect value="git clone git@github.com:jerome1232/PiCar.git"
		readonly size="41" id="ssh">
	</p>
	<div class="statusBar">
		<?php $ip = $_SERVER['SERVER_ADDR']; ?>
		System uptime: <?php echo shell_exec('uptime -p'); ?>
		Linux Kernel: <?php echo php_uname(); ?>
		Ip Address: <?php echo "server ip: $ip"; ?>
	</div>
</body>
</html>
