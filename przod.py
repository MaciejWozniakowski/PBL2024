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




publisher = rospy.Publisher('/revised_scan',LaserScan, queue_size=10)
scann=LaserScan()

def callback(data):

	main_maxx = odleglosc_przod=find_max_distance(data)   #// albo -1/8 i -3/8
	print(main_maxx)
	

def dane():
	rospy.init_node('revised_scan',anonymous=True)
	sub = rospy.Subscriber('/scan', LaserScan, callback)
	rospy.spin()
	

def find_max_distance(datas):
	maxx = -99999999
	n=len(datas.ranges)	
	kat = n/360
	for i in range(n*(-1)/8, n*1/8):
		a=datas.ranges[i-1]
		# print(a, i)
		if a > maxx and a < 10 and i >= -144 and i <= 142:
			maxx = a
			# print(maxx)
	return maxx



     
		

def main(args):

	
	dane()

	print("kuba")

if __name__=='__main__':
	main(sys.argv)