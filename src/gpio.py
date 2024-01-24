import RPi.GPIO as G
import sys
import time

DEFAULT_SEQ = [ 5, 6, 24, 19, 26 ]
DELAY = 0.1

args = sys.argv
prog = args.pop(0)

if len(args) == 1 and args[0] == '-h':
    print(f'usage:')
    print(f'\tf{prog}: <gpio0> <gpio1> ...')
    print()
    print(f'If pin numbers are omitted use default sequence of:')
    print(DEFAULT_SEQ)
    exit(-1)

seq = []
print(len(args))
if len(args) == 0:
    for i in range(len(DEFAULT_SEQ)):
        seq.append(DEFAULT_SEQ[i])
    print(f'{prog}: using default sequence {seq}')
else:
    while len(args) > 0:
        arg = args.pop(0)
        seq.append(int(arg))
    print(f'{prog}: using port sequence {seq}')

print(G.RPI_INFO)
print(G.VERSION)

G.setmode(G.BCM)
G.setwarnings(False)

class GpioArray:
    def __init__(self, seq, delay):
        self.sequence = seq
        self.delay = delay
        for channel in self.sequence:
            G.setup(channel, G.OUT, initial=G.HIGH)
            G.output(channel, G.LOW)
    
    def light_show(self):
        for channel in self.sequence:
            time.sleep(self.delay)
            G.output(channel, G.HIGH)
            time.sleep(self.delay)
            G.output(channel, G.LOW)

    def __del__(self):
        for channel in self.sequence:
            G.output(channel, G.LOW)
            G.cleanup(channel)

def demo():
    g = GpioArray(seq, 0.1)
    for i in range(10):
        g.light_show()

if __name__ == '__main__':
    demo()
