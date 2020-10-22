import pytest
from DriverClass import IM871A
from main import *

def test_driver():
    # Instantiate DriverClass 
    USBport = IM871A('/dev/ttyUSB0')

    # Testing ping
    assert USBport.ping() == True
    
    # Testing Linkmode
    assert USBport.setup_linkmode('s1') == True
    assert USBport.setup_linkmode('s1m') == True
    assert USBport.setup_linkmode('s2') == True
    assert USBport.setup_linkmode('t1') == True
    assert USBport.setup_linkmode('t2') == True
    assert USBport.setup_linkmode('c2a') == True
    assert USBport.setup_linkmode('c2b') == True
    assert USBport.setup_linkmode('c1a') == True
    assert USBport.setup_linkmode('c1b') == True
    assert USBport.setup_linkmode('ha') == False
    assert USBport.setup_linkmode('') == False

    # Closing port to test open function
    USBport.close()
    assert USBport.open() == True

    # Testing reset
    assert USBport.reset_module() == True

    # Testing several functions
    assert test1() == True
    
   

