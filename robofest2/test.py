#!/usr/bin/python
# -*- coding: utf-8 -*-

from chassis import *
from time import sleep

init()

while 1:
	move(1300, 700)
	while is_busy():
		sleep(0.1)

	turn(1200, 180)
	while is_busy():
		sleep(0.1)


