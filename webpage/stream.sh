#!/bin/sh
mjpg_streamer -o "output_http.so -w /usr/local/www" -i "input_raspicam.so -fps 30 -hf -vf -x 800 -y 600 ifx denoise"
exit 0
