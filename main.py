#!/usr/bin/env python
import roslib
import sys 
import rospy
import cv2 as cv
import time

from sensor_msgs.msg import LaserScan
import sensor_msgs.msg
import math
from geometry_msgs.msg import Twist

import select, termios, tty

from simple_pid import PID









publisher = rospy.Publisher('/revised_scan',LaserScan, queue_size=10)
scann=LaserScan()

#print("kuba") 

def LiczenieSredniejLewo(datas):
	x=0
	n=len(datas.ranges)	
	c_suma=2
	kat = n/360
	for i in range(n/8, n*2/8):
		a=datas.ranges[i-1]
		b=datas.ranges[i]
		c=b*a*math.sin(math.radians(kat))/(math.sqrt(a*a+b*b-2*a*b*math.cos(math.radians(kat))))
		if math.isnan(c) == False:
			c_suma=c_suma+c
			x=x+1
		
	c_avr=c_suma/x
	return c_avr

def LiczenieSredniejPrawo(datas):
	x=0
	n=len(datas.ranges)	
	c_suma=2
	kat = n/360
	for i in range(n*6/8, n*7/8):
		a=datas.ranges[i-1]
		b=datas.ranges[i]
		c=b*a*math.sin(math.radians(kat))/(math.sqrt(a*a+b*b-2*a*b*math.cos(math.radians(kat))))
		if math.isnan(c) == False:
			c_suma=c_suma+c
			x=x+1
		
	c_avr=c_suma/x
	return c_avr

def LiczenieSredniejSrodek(datas):
	x=1
	n=len(datas.ranges)	
	c_suma=2
	kat = n/360
	for i in range(n*(-1)/8, n*1/8):
		a=datas.ranges[i-1]
		b=datas.ranges[i]
		c=b*a*math.sin(math.radians(kat))/(math.sqrt(a*a+b*b-2*a*b*math.cos(math.radians(kat))))
		if math.isnan(c) == False:
			c_suma=c_suma+c
			x=x+1
	print(x)	
	c_avr=c_suma/x
	return c_avr

def callback(data):
	#n=len(data.ranges)
	x=1.0/8.0
	odleglosc_lewo=LiczenieSredniejLewo(data)
	odleglosc_prawo=LiczenieSredniejPrawo(data)  #//albo -1/8 i -3/8 
	odleglosc_przod=LiczenieSredniejSrodek(data)   #// albo -1/8 i -3/8 
	print("lewo:")
	print odleglosc_lewo
	print("prawo:")
	print odleglosc_prawo
	print("przod:")
	print odleglosc_przod
#	ruch(odleglosc_przod,odleglosc_prawo,odleglosc_lewo)
	Peide(odleglosc_prawo,odleglosc_lewo,odleglosc_przod)

def dane():
	rospy.init_node('revised_scan',anonymous=True)
	sub = rospy.Subscriber('/scan', LaserScan, callback)
	rospy.spin()

#def ruch(odl_przod,odl_p,odl_l):
#
#
#	settings = termios.tcgetattr(sys.stdin)
#	pub = rospy.Publisher('cmd_vel', Twist,queue_size = 1)	
#	
#	twist = Twist()
#	print("dzien_dobry")
#	twist.linear.x = 0.2
#	if odl_przod <= 0.3:
#		twist.linear.x= 0.1
#		twist.angular.z = -1
#	if odl_przod <= 0.3:
#		twist.linear.x= 0.1
#		twist.angular.z = -1
#	if odl_l <= 0.5:
#		twist.angular.z = -1
#		twist.linear.x= 0.1
#	if odl_p <= 0.5:
#		twist.angular.z = 1
#		twist.linear.x= 0.1

#	pub.publish(twist)

#	print("kuba")











## PID jak przestanie dzialac to tutaj cos robilewm


pid = PID(5, 0.1, 0.05, setpoint=0.5)




def Peide(odl_p, odl_l, odl_przod):

	settings = termios.tcgetattr(sys.stdin)
	pub = rospy.Publisher('cmd_vel', Twist,queue_size = 1)	
	twist = Twist()


	twist.linear.x= 0.2
	twist.angular.z = pid(odl_p)

	if odl_przod <= 1 and odl_p <= 1:
		
		twist.linear.x= 0.1
		

	if odl_przod <= 1 and odl_l <=1:
		
		twist.linear.x= 0.1

#	if odl_przod <= 0.3:
#		
#		twist.angular.z = -pid(odl_p)
#		twist.linear.x = -0.1
		


#	elif odl_p <= 1:
#		
#		twist.angular.z = 1
#		twist.linear.x= 0.2
#		twist.angular.z = pid(odl_p)
	

	
	pub.publish(twist)

	


## koniec PID


def main(args):

	dane()

	print("kuba")

if __name__=='__main__':
	main(sys.argv)
