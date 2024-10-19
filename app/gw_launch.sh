#!/bin/sh
/mavlink-router/mavlink-routerd -c NULL -p $(sh /app/get_host_ip.sh rovers_1):5760 -p $(sh /app/get_host_ip.sh rovers_2):5760