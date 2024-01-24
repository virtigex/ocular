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

#channel = int(sys.argv[1])

print(G.RPI_INFO)
print(G.VERSION)

G.setmode(G.BCM)
G.setwarnings(False)


def prepare(sequence):
    for channel in sequence:
        G.setup(channel, G.OUT, initial=G.HIGH)
        G.output(channel, G.LOW)

def light_show(sequence):
    for channel in sequence:
        print(f'channel: {channel}')
        time.sleep(DELAY)
        G.output(channel, G.HIGH)
        time.sleep(DELAY)
        G.output(channel, G.LOW)

def cleanup(sequence):
    for channel in sequence:
        G.cleanup(channel)

if __name__ == '__main__':
    prepare(seq)
    for i in range(10):
        light_show(seq)
    cleanup(seq)


