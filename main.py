from microbit import *
from machine import time_pulse_us, reset
import utime
import music

# Config
START_ANGLE = 36
CAPTURE_ANGLE = 55
TRIGGER_CM = 5
WAKE_CM = 25
RESET_MS = 3500
RESET_STEPS = 10

# Servo control on pin1
pin1.set_analog_period(20)

def servo_write(angle):
    pulse_us = 500 + (angle * 2000) // 180
    duty = (pulse_us * 1023) // 20000
    pin1.write_analog(duty)
    sleep(300)
    pin1.write_analog(0)

def servo_write_slow(from_angle, to_angle, duration_ms):
    steps = 20
    step_ms = duration_ms // steps
    for i in range(steps + 1):
        angle = from_angle + (to_angle - from_angle) * i // steps
        pulse_us = 500 + (angle * 2000) // 180
        duty = (pulse_us * 1023) // 20000
        pin1.write_analog(duty)
        sleep(step_ms)
    pin1.write_analog(0)

def sonar_ping_cm():
    # Trigger pulse on pin14
    pin14.write_digital(0)
    utime.sleep_us(2)
    pin14.write_digital(1)
    utime.sleep_us(10)
    pin14.write_digital(0)
    # Read echo on pin13
    duration = time_pulse_us(pin13, 1, 30000)
    if duration < 0:
        return -1
    return (duration * 0.0343) / 2

WDT_MS = 8000

# Software watchdog — call wdt_kick() regularly; if 8s passes without a kick, reset
_wdt_last = utime.ticks_ms()
def wdt_kick():
    global _wdt_last
    _wdt_last = utime.ticks_ms()

def wdt_check():
    if utime.ticks_diff(utime.ticks_ms(), _wdt_last) > WDT_MS:
        reset()

# Init
servo_write(START_ANGLE)
display.off()
sleep(500)
wdt_kick()

# Main loop
while True:
    wdt_kick()
    wdt_check()

    # Phase 1: slow idle poll
    dist = sonar_ping_cm()
    if dist <= 0 or dist >= WAKE_CM:
        display.off()
        sleep(500)
        continue

    # Phase 2: something nearby — fast poll with display
    display.on()
    display.show(str(min(int(dist), 9)))

    if dist < TRIGGER_CM:
        music.play(['C4:1', 'E4:1', 'G4:1', 'B4:1', 'C5:4'], wait=True)
        servo_write_slow(START_ANGLE, CAPTURE_ANGLE, 350)
        step_ms = RESET_MS // RESET_STEPS
        for i in range(RESET_STEPS):
            wdt_kick()
            wdt_check()
            brightness = max(0, 9 - (i * 9 // (RESET_STEPS - 1)))
            ring = i * 3 // RESET_STEPS
            img = Image(5, 5)
            for row in range(5):
                for col in range(5):
                    layer = min(row, col, 4 - row, 4 - col)
                    if layer >= ring:
                        img.set_pixel(col, row, brightness)
            display.show(img)
            sleep(step_ms)
        servo_write(START_ANGLE)
        display.off()
        sleep(2000)

    sleep(100)
