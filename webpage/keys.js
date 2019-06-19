// So this is fairly simple. I've done very, very little
// research into how javascript works, how to write it etc...
// what I do know, is that document.addEventListener causes
// it to start listening for key strokes ;)
document.addEventListener('keydown', function(keyDown) {
	// This is grabbing a canvas object from the webpage
	// (see index.php to see where the canvas object comes from)
	// at anyrate this grabs that canvas object and sets it up
	// as a 2d drawing area.
	var canvas = document.getElementById("keyPressed");
	var ctx = canvas.getContext("2d");
	ctx.font = "30px Arial";
	// each of these if branches are pretty much the same
	// when a key is pressed, I clear what's in my canvas object
	// and write something to it. This is just for testing atm.
	// I intend in the future to call a php script that writes
	// what key was pressed to a unix domain socket.
	var x = canvas.width / 2;
	if (keyDown.keyCode == 65) {
		// This is for "A"
		$.ajax({
			type: 'POST',
			url: 'sock_write.php',
			data: {key: "aDown"},
			success: function(data) {
				ctx.clearRect(0, 0, canvas.width, canvas.height);
				ctx.fillText('A: Turning left', 10, 50);
				ctx.fillText(data, 10, 80);
			}
		});
	}
	else if (keyDown.keyCode == 68) {
		// This is for "D"
		$.ajax({
			type: 'POST',
			url: 'sock_write.php',
			data: {key: "dDown"},
			success: function(data) {
				ctx.clearRect(0, 0, canvas.width, canvas.height);
				ctx.fillText('D: Turning right', 10, 50);
				ctx.fillText(data, 10, 80);
			}
		});
	}
	else if (keyDown.keyCode == 87) {
		// This is for "W"
		$.ajax({
			type: 'POST',
			url: 'sock_write.php',
			data: {key: "wDown"},
			success: function(data) {
				ctx.clearRect(0, 0, canvas.width, canvas.height);
				ctx.fillText('W: Moving forward', 10, 50);
				ctx.fillText(data, 10, 80);
			}
		});
	}
	else if (keyDown.keyCode == 83) {
		// This is for "S"
		$.ajax({
			type: 'POST',
			url: 'sock_write.php',
			data: {key: "sDown"},
			success: function(data) {
				ctx.clearRect(0, 0, canvas.width, canvas.height);
				ctx.fillText('S: Moving backwords', 10, 50);
				ctx.fillText(data, 10, 80);
			}
		});
	}
	else if (keyDown.keyCode == 32) {
	// This is for "Space"
	$.ajax({
			type: 'POST',
			url: 'sock_write.php',
			data: {key: "spaceDown"},
			success: function(data) {
				ctx.clearRect(0, 0, canvas.width, canvas.height);
				ctx.fillText('Space: Stopping', 10, 50);
				ctx.fillText(data, 10, 80);
			}
		});
	}
	else if (keyDown.keyCode == 81) {
	// This is for "Q"
	$.ajax({
			type: 'POST',
			url: 'sock_write.php',
			data: {key: "qDown"},
			success: function(data) {
				ctx.clearRect(0, 0, canvas.width, canvas.height);
				ctx.fillText('Q: Killing python script', 10, 50);
				ctx.fillText(data, 10, 80);
			}
		});
	}
	else if (keyDown.keyCode == 82) {
		// This is for R
		$.ajax({
			type: 'POST',
			url: 'sock_write.php',
			data: {key: "rDown"},
			success: function(data) {
				ctx.clearRect(0, 0, canvas.width, canvas.height);
				ctx.fillText('R: Increasing speed', 10, 50);
				ctx.fillText(data, 10, 80);
			}
		});
	}
	else if (keyDown.keyCode == 70) {
		// This is for "F"
		$.ajax({
			type: 'POST',
			url: 'sock_write.php',
			data: {key: "fDown"},
			success: function(data) {
				ctx.clearRect(0, 0, canvas.width, canvas.height);
				ctx.fillText('F: Decreasing speed', 10, 50);
				ctx.fillText(data, 10, 80);
			}
		});
	}
	else if (keyDown.keyCode == 72) {
		// This is for "H"
		$.ajax({
			type: 'POST',
			url: 'sock_write.php',
			data: {key: "hDown"},
			success: fucntion(data) {
				ctx.clearRect(0, 0, canvas.width, canvas.height);
				ctx.fillText('Honking the horn', 10, 50);
				ctx.fillText(data, 10, 80);
			}
		})
	}
}, true);

document.addEventListener("keyup", function(keyUp) {
	var canvas = document.getElementById("keyPressed");
	var ctx = canvas.getContext("2d");
	ctx.font = "30px Arial";
	var x = canvas.width / 2;

	if (keyUp.keyCode == 65) {
		$.ajax({
			type: 'POST',
			url: 'sock_write.php',
			data: {key: "aUp"},
			success: function(data) {
				ctx.clearRect(0, 0, canvas.width, canvas.height);
				ctx.fillText('A: Cease the turn!', 10, 50);
				ctx.fillText(data, 10, 80);
			}
		});
	}
	else if (keyUp.keyCode == 68) {
		$.ajax({
			type: 'POST',
			url: 'sock_write.php',
			data: {key: "dUp"},
			success: function(data) {
				ctx.clearRect(0, 0, canvas.width, canvas.height);
				ctx.fillText('D: Cease the turn!', 10, 50);
				ctx.fillText(data, 10, 80);
			}
		});
	}
	else if (keyUp.keyCode == 87) {
		$.ajax({
			type: 'POST',
			url: 'sock_write.php',
			data: {key: "wUp"},
			success: function(data) {
				ctx.clearRect(0, 0, canvas.width, canvas.height);
				ctx.fillText('W: Cease the forward!', 10, 50);
				ctx.fillText(data, 10, 80);
			}
		});
	}
	else if (keyUp.keyCode == 83) {
		$.ajax({
			type: 'POST',
			url: 'sock_write.php',
			data: {key: "sUp"},
			success: function(data) {
				ctx.clearRect(0, 0, canvas.width, canvas.height);
				ctx.fillText('S: Cease the backward!', 10, 50);
				ctx.fillText(data, 10, 80);
			}
		})
	}
	else if (keyUp.keyCode == 72) {
		// This is for "H"
		$.ajax({
			type: 'POST',
			url: 'sock_write.php',
			data: {key: "hUp"},
			success: fucntion(data) {
				ctx.clearRect(0, 0, canvas.width, canvas.height);
				ctx.fillText('Cease the horn', 10, 50);
				ctx.fillText(data, 10, 80);
			}
		})
}, true);
