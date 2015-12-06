#!/bin/bash -i

cd /home/pi/babymon/agent
python3 agent.py --url=$1
echo 'Agent stopped, shutting down in 300 seconds'
sleep 300
shutdown -r now
