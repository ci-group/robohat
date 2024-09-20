# 2022-2823-01.RaspberryRoboHat_2

This a library written in Python to access the robohat hardware

version v0.6.1

Install latest Pi OS (https://www.raspberrypi.com/software/)

Fill in username: 	robo
Password: 		????

update package.

sudo apt update
sudo apt upgrade

remove old packages and install new one to resolve a depenency
sudo apt remove python3-rpi.gpio			
sudo apt install python3-rpi-lgpio


Be sure you update config.txt int the Raspberry boot partition.
This is to enable the I2C ports which are needed.

replace the /boot/firmware/config.txt with the the config.txt on this repo in setup_files dier, to enable the I2C ports and the SPI ports


create dir at user robo
	bin
	robohat
	
move files robo, servo, buzz_random into /home/robo/bin from thisn bin folder in this repo

add to /home/robo/.bashrc
	export PATH="/home/robo/bin:$PATH"
	
	
copy the dir robohatlib of this repo into the /home/robo/	
	
by entering the command
servo or robo you can test the robo

