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


	<?php
		$ip = $_SERVER['SERVER_ADDR'];
		echo "<br><br>";
		echo "<img src=\"http://$ip:8080/?action=stream\" />";
		echo "<p>";
		echo shell_exec('uptime -p');
		echo "<br>";
		echo php_uname();
		echo "<br>";
		$pidf_path = "tmp/pid";
		$pidf = fopen($pidf_path, "r");
		$pid = fread($pidf, filesize($pidf_path));
		fclose($pidf);
		echo "Previous PID: $pid, Killing it to ensure it is dead<br>";
		shell_exec("kill $pid");
		$cmd = "nohup ./robot_car.py >/dev/null 2>&1 &";
		echo "Starting python script<br>";
		shell_exec($cmd);
		echo "Script Started, ready to roll<br>";
		echo "If you kill the python script, just reload the page "
			. "it will be run automatically again";
		echo "<br>";
		echo "server ip: $ip";
		echo "</p>";
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
