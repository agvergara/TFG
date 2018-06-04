#!/bin/sh


start(){
        ip route replace 193.147.54.0/24 via 193.147.53.176
}

stop(){
        ip route del 193.147.54.0/24
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

