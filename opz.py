import mido
import time
from gpiozero import LED
# import threading

# get OPZ midi port
opz_input = list(filter(lambda name: "OP-Z" in name, mido.get_input_names()))[0]

# set cv gpio pin
cv_4ppq = LED(2)
cv_12ppq = LED(3)
cv_24ppq = LED(4)
led_status = LED(14)
led_status.on()

# initialize state
beats = 0
bpm_time = time.time_ns() / 1000000
clocks = 0
running = False

# send cv clock pulse
def cv_clock(ppq):
    if ppq == 4:
        cv_4ppq.on()
        cv_4ppq.off()
    if ppq == 12:
        cv_12ppq.on()
        cv_12ppq.off()
    if ppq == 24:
        cv_24ppq.on()
        cv_24ppq.off()

# run logic on each beat
def beat():
    if running:
        global bpm_time
        global beats

        # toggle status led
        led_status.toggle()

        # calculate bpm
        new_bpm_time = time.time_ns() / 1000000
        bpm = round(60 * 1000 / (new_bpm_time - bpm_time))
        bpm_time = new_bpm_time

        # debugging
        print(f'beat {beats}; bpm {bpm}')

        beats += 1

def reset():
    led_status.on()

    if running:
        cv_clock(4)
        cv_clock(12)
        cv_clock(24)
    
    beats = 0
    clocks = 0

# open the port and read the messages
try:
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
                if clocks % (24 / 4) == 0:
                    cv_clock(4)
                # 12 ppq
                if clocks % (24 / 8) == 0:
                    cv_clock(12)
                # 24 ppq
                if clocks % (24 / 24) == 0:
                    cv_clock(24)

                # quarter note/crotchet
                if clocks > 22:
                    beat()
                    clocks = 0
                else:
                    clocks += 1
except KeyboardInterrupt:
    led_status.off()
    print('bye!')
