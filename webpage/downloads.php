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
            <a href="#contact">Contact</a>
            <a href="#about">About</a>
        </div>
        <h2> Download project files </h2>
        <p>
            robot_car.py: 
            <a href="robot_car.py" download="robot_car.py">robot_car.py</a>
            Last modified: 
<?php
echo date("F d, Y: G:i:s a", filemtime("robot_car.py"))
?><br>
            index.html:
            <a href="index.html" download="index.html">index.html</a>
            Last modified:
<?php
echo date("F d, Y: G:i:s a", filemtime("index.html"))
?><br>
            startpi.php:
            <a href="startpi.php" download="startpi.php">startpi.php</a>
            Last modified:
<?php
echo date("F d, Y: G:i:s a", filemtime("startpi.php"))
?><br>
            styles.css:
            <a href="styles.css" download="styles.css">styles.css</a>
            Last modified:
<?php
echo date("F d, Y: G:i:s a", filemtime("styles.css"))
?><br>
        </p>
    </body>
</html>
