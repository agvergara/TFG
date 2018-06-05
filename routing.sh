#!/bin/sh
#This script creates routes at the start of the nodes

start(){
        ip route replace X.X.X.X/24 via Y.Y.Y.Y
}

stop(){
        ip route del X.X.X.X/24
}

case "$1" in
        start)
                start
                ;;
        stop)
                stop
                ;;
        *)
                echo "Usage: ./routing.sh {start|stop}"
                exit 1
                ;;

esac

exit 0

