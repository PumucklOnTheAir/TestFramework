#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Install python modules
pip3 install -r requirements.txt

# Install fftserver as service in systemd

file="/etc/systemd/system/fftserver.service"

# check if file exists.
if [  -f "$file" ] ; then
    # if exist remove the file
    rm "$file"
fi

echo "[Unit]
Description=Freifunk Testserver
After=syslog.target" >> "$file"

echo "[Service]
Type=simple
ExecStart=$DIR/start_server.py" >> "$file"

echo "[Install]
WantedBy=multi-user.target" >> "$file"

rm /bin/fftserver_alive
ln test_server_alive.py /bin/fftserver_alive
chmod 755 /bin/fftserver_alive

# activate service
systemctl enable fftserver
systemctl restart fftserver
