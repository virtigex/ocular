import asyncio
import cv2
import signal
import sys

RUNNING = True

def signal_handler(sig, frame):
    global RUNNING
    print('You pressed Ctrl+C!')
    RUNNING = False

signal.signal(signal.SIGINT, signal_handler)

def display_cam(camid):
    global RUNNING
    print(f'using cam {camid}')
    vid = cv2.VideoCapture(camid)
    while RUNNING:
        _ret, frame = vid.read()
        title = f'cam {camid}'
        cv2.imshow(title, frame)
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            RUNNING = False
    print('cleanup')
    vid.release() 
    cv2.destroyAllWindows()
    print('display_cam finished')

def list_ports():
    """
    Test the ports and returns a tuple with the available ports 
    and the ones that are working.
    """
    is_working = True
    dev_port = 0
    working_ports = []
    available_ports = []
    while is_working:
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            is_working = False
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                print(f'\t{dev_port}: reads images ({h} x {w})')
                working_ports.append(dev_port)
            else:
                available_ports.append(dev_port)
        dev_port +=1
    return available_ports,working_ports

if __name__ == "__main__":
    args = sys.argv
    prog = args.pop(0)
    camid = -1
    if len(args) == 1:
        try:
            camid = int(args[0])
        except ValueError:
            camid = -1
    if camid >= 0:
        print('Ctrl-C to exit')
        display_cam(camid)
        exit(0)
    else:
        print(f'usage: {prog} <cammid>')
        print('available cameras are:')
        list_ports()
        exit(-1)
