# opzync

sync your OPZ to other CV controlled synths, without an OPZ module!

## Installation

You'll need:

- raspberry pi
- jumper leads, aligator clips, etc.
- patch cables
- and led

On the raspberry pi, run:

```bash
sudo apt update

sudo apt install -y git python3 python3-pip python3-rtmidi
pip3 install mido

git clone https://github.com/lockness-Ko/opzync
cd opzync

sudo cp opzync.service /etc/systemd/system/
```

Then, plug in your patch cables to GPIO pins:

- 2 for 6ppq
- 3 for 12ppq
- 4 for 24ppq

To connect the patch cables, use the jumper leads and aligator clips to 
connect the selected pin the the TIP of the patch cable and a ground gpio 
pin to the SLEEVE of the patch cable

Refer to this for GPIO pinouts: [https://pinout.xyz/](https://pinout.xyz/)

Connect the flat side of the LED pin to ground and the round side to pin 14

To run opzync, **PLUG IN THE OPZ FIRST** and type

```bash
sudo systemctl start opzync
```

To stop, run

```bash
sudo systemctl stop opzync && ./kill_opzync.sh
```

To run opzync when you turn on the pi (e.g. for when you want to use it 
without a screen), type

```bash
sudo systemctl enable opzync
```

**REMEMBER TO ALWAYS PLUG IN THE OPZ BEFORE YOU RUN OPZYNC**

otherwise it wont work :)

## How does it work?

It converts usb midi clock messages into 12ppq, 24ppq, and 6ppq cv clock pulses
