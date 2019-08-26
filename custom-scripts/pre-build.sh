#!/bin/sh

#rede
cp $BASE_DIR/../custom-scripts/S41network-config $BASE_DIR/target/etc/init.d
chmod +x $BASE_DIR/target/etc/init.d/S41network-config

#StartServer
cp $BASE_DIR/../custom-scripts/StartServer $BASE_DIR/target/etc/init.d
chmod +x $BASE_DIR/target/etc/init.d/StartServer

#my_server.py
cp $BASE_DIR/../custom-scripts/my_server.py $BASE_DIR/target/usr
chmod +x $BASE_DIR/target/usr/my_server.py
