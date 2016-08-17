#!/usr/bin/env python

import sys
import time
import os
import urllib2 

def shutdownPi(why):

   sys.stdout.flush()
   time.sleep(10.0)

   os.system("sudo shutdown -h now")

def rebootPi(why):

   os.system("sudo shutdown -r now")


def checkInternetConnection():
    try:
        urllib2.urlopen("http://www.google.com").close()
    except urllib2.URLError:
        print "Internet Not Connected"
        time.sleep(1)
	return false
    else:
        print "Internet Connected"
	return true


WLAN_check_flg = 0

def WLAN_check():
        '''
        This function checks if the WLAN is still up by pinging the router.
        If there is no return, we'll reset the WLAN connection.
        If the resetting of the WLAN does not work, we need to reset the Pi.
        source http://www.raspberrypi.org/forums/viewtopic.php?t=54001&p=413095
        '''
	global WLAN_check_flg
        ping_ret = subprocess.call(['ping -c 2 -w 1 -q 192.168.1.1 |grep "1 received" > /dev/null 2> /dev/null'], shell=True)
	if ping_ret:
            # we lost the WLAN connection.
            # did we try a recovery already?
            if (WLAN_check_flg>2):
                # we have a serious problem and need to reboot the Pi to recover the WLAN connection
		print "logger WLAN Down, Pi cannot forcing a reboot"
                WLAN_check_flg = 0 
		# rebootPi("WLAN Down")
                #subprocess.call(['sudo shutdown -r now'], shell=True)
            else:
                # try to recover the connection by resetting the LAN
                #subprocess.call(['logger "WLAN is down, Pi is resetting WLAN connection"'], shell=True)
		print "WLAN Down, Pi is trying resetting WLAN connection"+ time.strftime("%Y-%m-%d %H:%M:%S")
                WLAN_check_flg = WLAN_check_flg + 1 # try to recover
                subprocess.call(['sudo /sbin/ifdown wlan0 && sleep 10 && sudo /sbin/ifup --force wlan0'], shell=True)
        else:
            WLAN_check_flg = 0
	    print "WLAN is OK"




print ""
print "Chicken cam"
print ""
print ""
print "Program Started at:"+ time.strftime("%Y-%m-%d %H:%M:%S")
print ""



secondCount = 1
while True:
	

	# every 5 minutes, check for shutdown


	if ((secondCount % (30*60)) == 0):
		# print every 900 seconds
    		WLAN_check()

    	#WLAN_check()


	# every 48 hours, reboot
	if ((secondCount % (60*60*48)) == 0):
		# reboot every 48() hours seconds
		rebootPi("48 hour reboot")		


	secondCount = secondCount + 1
	# reset secondCount to prevent overflow forever

	if (secondCount == 1000001):
		secondCount = 1	
	
	time.sleep(1.0)

