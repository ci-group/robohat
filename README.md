# 2022-2823-01.RaspberryRoboHat_2

This a library written in Python to access the robohat hardware

version v0.6.3

Install latest Pi OS (https://www.raspberrypi.com/software/) (at this moment bookwork, based on Debian 12)

Fill in username: 	robo
Password: 			????

update packages.

	sudo apt update
	sudo apt upgrade

remove old packages and install new one to resolve a depenency

	sudo apt remove python3-rpi.gpio
	sudo apt install python3-rpi-lgpio


Be sure you update config.txt int the Raspberry boot partition.
This is to enable the I2C ports which are needed.

replace the /boot/firmware/config.txt with the the config.txt on this repo in setup_files folder, to enable the I2C ports and the SPI ports

create dir at user robo

	mkdir /home/robo/bin
	mkdir /home/robo/robohat
	
move files robo, servo, buzz_random into /home/robo/bin from thisn bin folder in this repo

add to /home/robo/.bashrc

	export PATH="/home/robo/bin:$PATH"
	
	
copy the dir robohatlib of this repo into the /home/robo/robohat	

copy the dir testlib of this repo into /home/robo/robohat	
	
Make the files robo and servo executable

	sudo chmod +x /home/robo/bin/robo
	sudo chmod +x /home/robo/bin/servo
	
Copy SerTest.py into /home/robo/robohat	

Copy Test.py into /home/robo/robohat	
	
by entering the command
servo or robo you can test the robo

