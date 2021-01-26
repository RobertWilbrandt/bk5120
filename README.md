BK5120 test
===========

This package creates a small script for testing the Beckhoff BK5120 CANopen bus coupler.

Installation
------------

The easiest way to install this script is to use pip:

```console
$ git clone git@github.com:RobertWilbrandt/bk5120.git && cd bk5120  # Clone library
$ pip3 install --user -r requirements.txt  # Install requirements
$ pip3 install --user .  # Install library
```

CAN setup
---------

This script uses the socketcan framework. In order to use it, you first have to set up your interface.

You can find your interface name using the ```ip addr``` command (for most users this will just be ```can0```). With this info execute

```console
$ sudo ip link set <interface> up type can bitrate <bitrate>  # Match configured bitrate
$ sudo ip link set <interface> txqueuelen 1000  # Not always needed, but common problem
```
