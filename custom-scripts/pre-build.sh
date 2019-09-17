#!/bin/sh

#rede
cp $BASE_DIR/../custom-scripts/S41network-config $BASE_DIR/target/etc/init.d
chmod +x $BASE_DIR/target/etc/init.d/S41network-config

#StartServer
cp $BASE_DIR/../custom-scripts/S42start-server $BASE_DIR/target/etc/init.d
chmod +x $BASE_DIR/target/etc/init.d/S42start-server

#my_server.py
cp $BASE_DIR/../custom-scripts/my_server.py $BASE_DIR/target/usr/bin
chmod +x $BASE_DIR/target/usr/bin/my_server.py

#Compile the syscall_test.c
BUILDROOT_DIR=$BASE_DIR/..
COMPILER=$BUILDROOT_DIR/output/host/bin/i686-buildroot-linux-uclibc-gcc
$COMPILER -o $BUILDROOT_DIR/output/target/bin/syscall_test $BUILDROOT_DIR/custom-scripts/syscall_test.c

#make simple-driver
make -C $BASE_DIR/../modules/simple_driver/
