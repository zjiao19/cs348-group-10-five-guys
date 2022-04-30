#!/usr/bin/env bash

for pid in $(ps ax | awk '/runserver 0.0.0.0:80/ {print $1}'); do
    sudo kill $pid 2>&-
done
cd /var/five_guys
nohup sudo /bin/python3 /var/five_guys/manage.py runserver 0.0.0.0:80 >> /var/five_guys/server.log 2>&1 &
echo '[Restarting Server] output redirected to server.log'
echo $PS1
