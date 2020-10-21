"""
Generic driver class for WM-Bus USB-dongle IM871A 
*************************************************
:platform: Python 3.5.10 on Linux, OS X
:synopsis: This module implements a class for communication with IM871A module.
:authors: Steffen Breinbjerg, Thomas Serup
:date: 21 October 2020


Link Modes
===============
IM871A is able to run in different modes. Default mode is S2.
+-----------------------+----------+-------------------------------------------------------+
| Mode                  | Argument | Description                                           |
+=======================+==========+=======================================================+
| S1                    | s1       | Stationary, one way communication                     |
+-----------------------+----------+-------------------------------------------------------+
| S1-m                  | s1m      | S1 with shorter header                                |
+-----------------------+----------+-------------------------------------------------------+
| S2                    | s2       | Stationary, bidirectional communication               | 
+-----------------------+----------+-------------------------------------------------------+
| T1                    | t1       | Frequent transmit, one way communication              | 
+-----------------------+----------+-------------------------------------------------------+
| T2                    | t2       | Frequent transmit, bidirectional communication        |  
+-----------------------+----------+-------------------------------------------------------+
| C1, Telegram Format A | c1a      | Compact, one way communication. No fixed length       | 
+-----------------------+----------+-------------------------------------------------------+
| C1, Telegram Format B | c1b      | Compact, bidirectional communication. Fixed length    | 
+-----------------------+----------+-------------------------------------------------------+
| C2, Telegram Format A | c2a      | Compact, one way communication. No fixed length       | 
+-----------------------+----------+-------------------------------------------------------+
| C2, Telegram Format B | c2b      | Compact, bidirectional communication. Fixed length    | 
+-----------------------+----------+-------------------------------------------------------+


"""
import serial as port
import sys
import struct
import time
import argparse
from macros import *
   
class IM871A:  
    """
    Implementation of a driver class for IM871A USB-dongle. 
    Takes path to IM871A as argument, e.g. '/dev/ttyUSB1'.
    """ 

    def __init__(self, Port): 
        self.Port = Port 
        self.__init_open(Port)


    def __init_open(self, Port: str) -> bool:
        """
        Initially creates and open serial communication with USB-dongle.
        Takes the port path as input.
        This function is only run once when class is instantiated. 
        If port is closed after instantiation, use open() function to reopen port.
        """       
        try:
            self.IM871 = port.Serial(port=Port, baudrate=57600, bytesize=8, parity=port.PARITY_NONE, stopbits=1, timeout=0)
            print("Connected to Serial port " + Port)
            return True
        except (ValueError, port.SerialException) as err:
            print(err)
            return False


    def __string_to_hex(self, argument: str) -> bytes:
        """
        Convert 'mode' argument into bytes. Returns '0xa' if no valid input.
        Function is used in 'setup_linkmode()'.
        """
        switcher = {
            's1' : 0x0, 
            's1m': 0x1, 
            's2' : 0x2, 
            't1' : 0x3, 
            't2' : 0x4, 
            'c1a': 0x6, 
            'c1b': 0x7, 
            'c2a': 0x8, 
            'c2b': 0x9
            }
        return switcher.get(argument, 0xa)


    def read_data(self) -> None:
        """
        Read data from all meters sending with the specified link mode.
        """
        while True:
            try:
                data = self.IM871.read(100)
            except port.SerialException as err:
                print(err)
                return  

            # Only print out if data has any content      
            if len(data) != 0:
                data_conv = data.hex()
                print(data_conv)


    def ping(self) -> bool:
        """
        Ping the WM-Bus module to check if it's alive.
        """
        try:
            self.IM871.write(port.to_bytes([IM871A_SERIAL_SOF, DEVMGMT_ID, DEVMGMT_MSG_PING_REQ, 0x0]))
        except port.SerialTimeoutException as err:
            print(err)
            return False

        # Looking for response message from IM871A
        for _ in range(0, 500):
            try:
                data = self.IM871.read(10)
            except port.SerialException as err:
                print(err)
                return False
            data_conv = data.hex()
            # Looking for Endpoint-ID and Msg-ID in response
            if(data_conv[3:6] == "102"):
                print("Ping Response received")
                return True

        # If no response message arrives        
        print("!No response from WM-Bus module")
        return False


    def reset_module(self) -> bool:
        """
        Reset the WM-Bus module.
        The reset will be performed after approx. 500ms.
        """ 
        try:
            self.IM871.write([IM871A_SERIAL_SOF, DEVMGMT_ID, DEVMGMT_MSG_RESET_REQ, 0x00])
        except port.SerialTimeoutException as err:
            print(err)
            return False

        # Looking for response message from IM871A    
        for _ in range(0, 500):
            try:
                data = self.IM871.read(10)
            except port.SerialException as err:
                print(err)
                return False
            data_conv = data.hex()
            # Looking for Endpoint-ID and Msg-ID in response
            if(data_conv[3:6] == "108"):
                print("Module resetting...")
                return True

        # If no response message arrives
        print("!Module won't reset")
        return False


    def setup_linkmode(self, mode: str) -> bool:
        """
        Setup link mode for communication with meter. 
        Takes the link mode as argument.
        If no Link Mode is set, default is 'S2'
        """
        # Converting mode-string to byte
        Mode = self.__string_to_hex(mode)
        if(Mode == 0xa):
            print("!Invalid link mode")
            return False
        try:
            self.IM871.write(port.to_bytes([IM871A_SERIAL_SOF, DEVMGMT_ID, DEVMGMT_MSG_SET_CONFIG_REQ, 0x03, TEMP_MEM, 0x2, Mode]))
        except port.SerialTimeoutException as err:
            print(err)
            return False

        # Looking for responce message from IM871A     
        for _ in range(0, 500):
            try:
                data = self.IM871.read(10)
            except port.SerialException as err:
                print(err)
                return False
            data_conv = data.hex()
            # Looking for Endpoint-ID and Msg-ID in response
            if(data_conv[3:6] == "104"):
                print("Link mode set to " + mode)
                return True

        # If no responce message arrives
        print("!Failed to setup link mode")
        return False
        

    def open(self):
        """
        Opens the port if port has been closed.
        It opens with the path given when instantiating the class.
        """
        try:
            self.IM871.open()
            print("Port " + self.Port + " is opened")
        except port.SerialException as err:
            print(err)


    def close(self):
        """
        Close the port
        """
        self.IM871.close()
        print("Port " + self.Port + " is closed")
