import mido
import time
from gpiozero import LED
# import threading

# get OPZ midi port
opz_input = list(filter(lambda name: "OP-Z" in name, mido.get_input_names()))[0]

# set cv gpio pin
cv_pin = LED(2)

# initialize state
beats = 0
bpm_time = time.time_ns() / 1000000
clocks = 0
running = False

# send cv clock pulse
def cv_clock():
    cv_pin.on()
    cv_pin.off()

# run logic on each beat
def beat():
    if running:
        global bpm_time
        global beats

        print("beat")

        # calculate bpm
        new_bpm_time = time.time_ns() / 1000000
        bpm = round(60 * 1000 / (new_bpm_time - bpm_time))
        bpm_time = new_bpm_time
        print(bpm)

        beats += 1

def reset():
    beats = 0
    clocks = 0

# open the port and read the messages
with mido.open_input(opz_input) as opz:
    for msg in opz:
        if msg.type in ["start", "stop"]:
            print(msg.type)

            # if start msg, start sending clock pulses
            running = True if msg.type == "start" else False
            beat()

            # reset clocks and beats
            reset()
        elif msg.type == "clock":
            if not running: continue
            # 4 ppq
            if clocks % 6 == 0:
                cv_clock()
            # 24 ppq
            if clocks > 22:
                beat()
                clocks = 0
            else:
                clocks += 1
