import serial as port
import sys
import struct
import time
import argparse
from macros import *

# Parse commandline arguments
#parser = argparse.ArgumentParser()
#parser.add_argument("SerialNo", help="Meter serial number")
#args = parser.parse_args()

    
class IM871A:  
    """Driver class for IM871A USB-dongle""" 

    IM871 = None

    def open(self):
        """Create and open serial communication with USB-dongle"""
        self.IM871 = port.Serial(port='/dev/ttyUSB0', baudrate=57600, bytesize=8, parity=port.PARITY_NONE, stopbits=1, timeout=0) 
        try:
            self.IM871.isOpen()
            print("Connected to Serial port ttyUSB0")
        except IOError:
            sys.exit("Failed to open the USB port")


    def read_data(self):
        """Read data from all meters"""
        while True:
            data = self.IM871.read(100)
            if len(data) != 0:
                datasci = data.hex()
                print(datasci)


    def close(self):
        self.IM871.close()

    

# Running necessary functions 
myDongle = IM871A()

myDongle.open()
myDongle.read_data()
myDongle.close()


