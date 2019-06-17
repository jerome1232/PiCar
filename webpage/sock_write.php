<?php
	$data = $_POST['key'];
	$sock = socket_create(AF_UNIX, SOCK_STREAM, 0);
	if (!$sock)
	{
		echo "socket_create() failed: "
		. socket_strerror(socket_last_error());
	}
	$path = $_SERVER['DOCUMENT_ROOT']."/tmp/pySock";
	if (socket_connect($sock, $path) == false)
	{
		echo "socket_connect() failed: "
		. socket_strerror(socket_last_error());
	}
	else
	{
		socket_write($sock, $data);
		socket_shutdown($sock);
		socket_close($sock);
	}
?>
