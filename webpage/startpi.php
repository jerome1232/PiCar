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
            <a href="downloads.php">Downloads</a>
            <a href="#contact">Contact</a>
            <a href="#about">About</a>
        </div>
<?php
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
    echo "If you kill the python script, just reload the page it will be run automatically again";
    echo "</p>"
?>
    <script src='jquery/jquery-3.3.1.js'></script>
    <script src='keys.js'></script></body>
    
    <p>
    <canvas id="keyPressed")
        width="600px"
        height="100px">
    </canvas>
    </p>
    <footer>
        <address>
            Written by <a href="mailto:j.jones1232@gmail.com">Jeremy Jones</a>.<br>
            Last modified: Mon Spetember 3<sup>rd</sup> 2018.
        </address>
    </footer>
</html>
