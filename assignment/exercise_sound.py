#!/usr/bin/env python3
"""
PWM Tone Generator

based on https://www.coderdojotc.org/micropython/sound/04-play-scale/
"""

import machine
import utime

# GP16 is the speaker pin
SPEAKER_PIN = 16

# create a Pulse Width Modulation Object on this pin
speaker = machine.PWM(machine.Pin(SPEAKER_PIN))


def playtone(frequency: float, duration: float) -> None:
    speaker.duty_u16(1000)
    speaker.freq(frequency)
    utime.sleep(duration)


def quiet():
    speaker.duty_u16(0)

c4 = 262
d4 = 294
e4 = 330
f4 = 349
g4 = 392
a4 = 440
b4 = 494
c5 = 523
d5 = 587
e5 = 659
f5 = 698
g5 = 784
a5 = 880
b5 = 988

notes = [e4, g4, a4, a4, 0, a4, b4, c5, c5, 0, c5, d5, b4, b4, 0, a4, g4, a4, 0, e4, g4, a4, a4, 0, a4, b4, c5, c5, 0, c5, d5, b4, b4, 0, a4, g4, a4, 0, e4, g4, a4, a4, 0, a4, c5, d5, d5, 0, d5, e5, f5, f5, 0, e5, d5, e5, a4, 0, a4, b4, c5, c5, 0, d5, e5, a4, 0, a4, c5, b4, b4, 0, c5, a4, b4, 0, a4, a4]
durations = [125, 125, 250, 125, 125, 125, 125, 250, 125, 125, 125, 125, 250, 125, 125, 125, 125, 375, 125, 125, 125, 250, 125, 125, 125, 125, 250, 125, 125, 125, 125, 250, 125, 125, 125, 125, 375, 125, 125, 125, 250, 125, 125, 125, 125, 250, 125, 125, 125, 125, 250, 125, 125, 125, 125, 125, 250, 125, 125, 125, 250, 125, 125, 250, 125, 250, 125, 125, 125, 250, 125, 125, 125, 125, 375, 375, 250, 125]

freq: float = 30
duration: float = 0.1  # seconds

print("Playing frequency (Hz):")

for i in range(78):
    if notes[i]==0:
        utime.sleep(durations[i]*0.001)
    else:
        playtone(notes[i], durations[i]*0.001)
    print(notes[i])
    #playtone(notes[i], durations[i]*0.001)
    #freq = int(freq * 1.1)

# Turn off the PWM
quiet()
