import usb.core

# with pure PyUSB
for dev in usb.core.find(find_all=True):
    print(dev)
