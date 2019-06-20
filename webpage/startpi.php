<!DOCTYPE HTML>
<html>
<head>
		<link rel="stylesheet" href="styles.css" />
		<meta name="viewport"
				content="viewport"
				charset="UTF-8">
</head>
<body>
	<!-- This is the top navigation bar -->
	<div class="topnav">
			<a href="index.html">Home</a>
			<a class="active" href="startpi.php">PiCar</a>
			<a href="joystick.html">Joystick Testing</a>
			<a href="downloads.php">Downloads</a>
			<a href="#contact">Contact</a>
			<a href="#about">About</a>
	</div>
	<!-- Where mjpeg stream shows from Pi camera -->
	<div class="pi-stream">
		<?php
			/**
			* Get local ip address and insert it into img tag
			* so that when dhcp changes ip address, the img tag doesn't have
			* to be manually updated. This is for the mjpeg stream from camera.
			*/
			$ip = $_SERVER['SERVER_ADDR'];
			echo "<img src=\"http://$ip:8080/?action=stream\" />";
		?>
	</div>
	<!-- The below displays some server information in a status bar.
		I plan to put a battery indicator here as well. -->
	<div class="statusBar">
		System uptime: <?php echo shell_exec('uptime -p'); ?>
		Linux Kernel: <?php echo php_uname(); ?>
		Ip Address: <?php echo "server ip: $ip"; ?>
	</div>
	<?php
		/*
		* Open a file that contains previous PID of python script.
		* Close PID file
		* kill the previous PID to ensure script isn't still running.
		*/
		$pidf_path = "tmp/pid";
		$pidf = fopen($pidf_path, "r");
		$pid = fread($pidf, filesize($pidf_path));
		fclose($pidf);
		shell_exec("kill $pid");
		/* Run python script to start robot_car */
		$cmd = "nohup pyScripts/robot_car.py >/dev/null 2>&1 &";
		shell_exec($cmd);
	?>
<script src='jquery/jquery-3.3.1.js'></script>
<script src='keys.js'></script></body>
<p>
<canvas id="keyPressed")
	width="600px"
	height="100px">
</canvas>
</p>
</body>
<footer>
	<address>
		Written by <a href="mailto:j.jones1232@gmail.com">Jeremy Jones</a>.<br>
		Last modified: Mon June 6<sup>th</sup> 2019.
	</address>
</footer>
</html>
