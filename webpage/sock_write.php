<?php
$data = $_POST['key'];
$sock = socket_create(AF_UNIX, SOCK_STREAM, 0);
$path = $_SERVER['DOCUMENT_ROOT'].'/tmp/pySock';
if (socket_connect($sock, $path) === false) {
	echo "Connection failed";
} else {
	socket_write($sock, $data);
	socket_shutdown($sock);
	socket_close($sock);
}
?>
