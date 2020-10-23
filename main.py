from Driver.DriverClass import IM871A
import time


def test1() -> bool:
    USB_port_0 = IM871A('/dev/ttyUSB0')
    check1 = USB_port_0.reset_module()      
    # Needs time after reset before being able to setup linkmode
    time.sleep(4)
    check2 = USB_port_0.setup_linkmode('c1a')
    if(check1 & check2):
        return True
    return False


if __name__ == '__main__':
    myUSB = IM871A('/dev/ttyUSB0')
    myUSB.reset_module()      
    # Needs time after reset before being able to setup linkmode
    time.sleep(4)
    myUSB.setup_linkmode('c1a')
    myUSB.read_data()


