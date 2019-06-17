<?php
	$data = $_POST['key'];
	if (($sock = socket_create(AF_UNIX, SOCK_STREAM, 0)) == false)
	{
		echo "socket_create() failed: "
		. socket_strerror(socket_last_error()) . "/n";
		exit();
	}
	$path = $_SERVER['DOCUMENT_ROOT'].'/tmp/pySock';
	if (socket_connect($sock, $path) == false) {
		echo "Connection failed: "
		. socket_strerror(socket_last_error()) . "/n";
	} else {
		socket_write($sock, $data);
		socket_shutdown($sock);
		socket_close($sock);
	}
?>
