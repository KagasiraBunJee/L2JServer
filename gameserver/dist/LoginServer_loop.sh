#!/bin/bash

err=1
until [ $err == 0 ]; 
do
	[ -f log/java0.log.0 ] && mv log/java0.log.0 "log/`date +%Y-%m-%d_%H-%M-%S`_java.log"
	[ -f log/stdout.log ] && mv log/stdout.log "log/`date +%Y-%m-%d_%H-%M-%S`_stdout.log"
	java -Xms128m -Xmx128m -cp lib/*:l2jfrozen-core.jar com.l2jfrozen.loginserver.L2LoginServer
# debug with IntelliJ Debugger
#	java -Xdebug -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=127.0.0.1:5005 -Xms128m -Xmx128m -cp lib/*:l2jfrozen-core.jar com.l2jfrozen.loginserver.L2LoginServer
	err=$?
#	/etc/init.d/mysql restart
	sleep 10;
done
