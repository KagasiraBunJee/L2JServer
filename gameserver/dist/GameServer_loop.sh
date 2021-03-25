#!/bin/bash

DBHOST=localhost
USER=root
PASS=
DBNAME=l2jdb

err=1
until [ $err == 0 ];
do
        #mysqlcheck -h $DBHOST -u $USER --password=$PASS -s -r $DBNAME>>"log/`date +%Y-%m-%d_%H:%M:%S`-sql_check.log"
        #mysqldump -h $DBHOST -u $USER --password=$PASS $DBNAME|zip "backup/`date +%Y-%m-%d_%H:%M:%S`-l2jdb_gameserver.zip" -
        [ -f log/java0.log.0 ] && mv log/java0.log.0 "log/`date +%Y-%m-%d_%H-%M-%S`_java.log"
        [ -f log/stdout.log ] &&  mv log/stdout.log "log/`date +%Y-%m-%d_%H-%M-%S`_stdout.log"
        [ -f log/chat.log ] && mv log/chat.log "log/`date +%Y-%m-%d_%H:%M:%S`-chat.log"
        java -Dfile.encoding=UTF- -Xms1024m -Xmx1024m -cp lib/*:lib/uMad/*:l2jfrozen-core.jar com.l2jfrozen.gameserver.GameServer
#        java -Xdebug -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=127.0.0.1:5006 -Dfile.encoding=UTF- -Xms1024m -Xmx1024m -cp lib/*:lib/uMad/*:l2jfrozen-core.jar com.l2jfrozen.gameserver.GameServer
        err=$?
        sleep 10
done
