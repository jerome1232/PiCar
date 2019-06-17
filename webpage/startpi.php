<!DOCTYPE HTML>
<html>
<head>
		<link rel="stylesheet" href="styles.css" />
		<meta name="viewport"
				content="viewport"
				charset="UTF-8">
</head>
<body>
	<div class="topnav">
			<a href="index.html">Home</a>
			<a class="active" href="startpi.php">PiCar</a>
			<a href="joystick.html">Joystick Testing</a>
			<a href="downloads.php">Downloads</a>
			<a href="#contact">Contact</a>
			<a href="#about">About</a>
	</div>
	<div class="pi-stream">
		<?php
			$ip = $_SERVER['SERVER_ADDR'];
			echo "<img src=\"http://$ip:8080/?action=stream\" />";
		?>
	</div>
	<div class="statusBar">
		System uptime: <?php echo shell_exec('uptime -p'); ?>
		Linux Kernel: <?php echo php_uname(); ?>
		Ip Address: <?php echo "server ip: $ip"; ?>
		Document Root: <?php echo "$_SERVER['DOCUMENT_ROOT']"; ?>
	</div>
	<?php
		$pidf_path = "tmp/pid";
		$pidf = fopen($pidf_path, "r");
		$pid = fread($pidf, filesize($pidf_path));
		echo "Previous PID: " . $pid;
		fclose($pidf);
		shell_exec("kill $pid");
		$cmd = "nohup ./robot_car.py >/dev/null 2>&1 &";
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
