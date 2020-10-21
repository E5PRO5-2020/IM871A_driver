from DriverClass import IM871A


USB_port_0 = IM871A('/dev/ttyUSB0')
#USB_port_0.reset_module()
#USB_port_0.setup_linkmode('c1a')
#USB_port_0.open()
USB_port_0.ping()
#USB_port_0.close()
USB_port_0.read_data()