import smbus
import math
import os
import logging

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

logging.basicConfig(filename='mpu9150.log',level=logging.DEBUG,format='%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')

while True:
	os.system('clear')
	print "Logging IMU"
	
	gyro_xout = read_word_2c(0x43)
	gyro_yout = read_word_2c(0x45)
	gyro_zout = read_word_2c(0x47)
	
	scale_gyro_xout = (gyro_xout / 131)
	scale_gyro_yout = (gyro_yout / 131)
	scale_gyro_zout = (gyro_zout / 131)
	
	logging.info(">> gyro_xout: "+ str(gyro_xout)+ " scaled: "+ str(scale_gyro_xout))
	logging.info(">> gyro_yout: "+ str(gyro_yout)+ " scaled: "+ str(scale_gyro_yout))
	logging.info(">> gyro_zout: "+ str(gyro_zout)+ " scaled: "+ str(scale_gyro_zout))
	
	accel_xout = read_word_2c(0x3b)
	accel_yout = read_word_2c(0x3d)
	accel_zout = read_word_2c(0x3f)
	
	accel_xout_scaled = accel_xout / 16384.0
	accel_yout_scaled = accel_yout / 16384.0
	accel_zout_scaled = accel_zout / 16384.0
	
	logging.info(">> accel_xout: "+ str(accel_xout)+ " scaled: "+ str(accel_xout_scaled))
	logging.info(">> accel_yout: "+ str(accel_yout)+ " scaled: "+ str(accel_yout_scaled))
	logging.info(">> accel_zout: "+ str(accel_zout)+ " scaled: "+ str(accel_zout_scaled))
	
	logging.info(">> x rotation: " + str(get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)))
	logging.info(">> y rotation: " + str(get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)))
