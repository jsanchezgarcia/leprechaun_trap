# Leprechaun Trap

Sonar-triggered servo trap running on a BBC micro:bit V2. When something gets within 5cm of the sonar, the servo actuates, a melody plays, and the LED grid counts down before resetting.

---

## Hardware

| Part | Notes |
|---|---|
| BBC micro:bit **V2** | Must be V2 — this uses the built-in speaker |
| HC-SR04 ultrasonic sonar | 4 pins: VCC, GND, Trig, Echo |
| Servo motor | Standard 5V servo |
| 2× AAA battery pack | Powers the micro:bit |

### Wiring

```
HC-SR04
  VCC  → 3V  (micro:bit)
  GND  → GND (micro:bit)
  Trig → P14 (micro:bit)
  Echo → P13 (micro:bit)

Servo
  Signal → P1  (micro:bit)
  VCC    → 3V  (micro:bit)
  GND    → GND (micro:bit)
```

> **Note:** If the servo is too weak or jittery from the micro:bit's 3V rail, power its VCC from the battery pack directly and share GND with the micro:bit.

---

## First-time setup (new machine)

### 1. Install Python 3

Check if you have it:
```bash
python3 --version
```
If not, install via [python.org](https://python.org) or `brew install python` on macOS.

### 2. Create a virtual environment and install tools

```bash
python3 -m venv ~/microbit-venv
source ~/microbit-venv/bin/activate
pip install uflash microfs pyserial
```

> You'll need to `source ~/microbit-venv/bin/activate` each new terminal session, or just use the full path `~/microbit-venv/bin/uflash` etc.

### 3. Flash MicroPython firmware onto the micro:bit

This only needs to be done once (or when switching from MakeCode back to MicroPython).

Plug in the micro:bit via USB. It mounts as a drive called `MICROBIT`.

```bash
~/microbit-venv/bin/uflash
```

This flashes the MicroPython runtime. The micro:bit reboots and the `MICROBIT` drive reappears.

### 4. Upload the script

```bash
~/microbit-venv/bin/ufs put main.py
```

### 5. Run it

Press the **reset button on the back** of the micro:bit, or send a soft reset over serial:

```bash
python3 -c "
import serial, time
ser = serial.Serial('/dev/tty.usbmodem*', 115200, timeout=3)
ser.write(b'\x03\x03'); time.sleep(1); ser.read(ser.in_waiting)
ser.write(b'\x04')
ser.close()
"
```

> On macOS, find the serial port with: `ls /dev/tty.usbmodem*`

---

## Iterating (day-to-day workflow)

Edit `main.py`, then:

```bash
~/microbit-venv/bin/ufs put main.py
```

Then reset the micro:bit (reset button or serial Ctrl+D). No cloud compile, no USB drag-and-drop — takes about 2 seconds.

---

## Behavior

| State | What happens |
|---|---|
| Idle (nothing within 25cm) | Display off, sonar pings every 500ms |
| Active (within 25cm) | Display on, shows distance in cm (capped at 9) |
| Triggered (within 5cm) | Plays melody → servo actuates → LED grid shrinks/dims over 3.5s → servo resets → 2s cooldown |

---

## Configuration

All tunable values are at the top of `main.py`:

| Variable | Default | Description |
|---|---|---|
| `START_ANGLE` | 36 | Servo resting angle (degrees) |
| `CAPTURE_ANGLE` | 55 | Servo triggered angle (degrees) |
| `TRIGGER_CM` | 5 | Distance to trigger (cm) |
| `WAKE_CM` | 25 | Distance to wake display (cm) |
| `RESET_MS` | 3500 | Countdown duration before servo resets (ms) |
| `RESET_STEPS` | 10 | Number of animation steps in the countdown |

---

## Choosing a melody

Open `melodies.html` in any browser. Click ▶ to preview melodies, click a card to select, then **Copy** to get the `music.play(...)` line. Paste it into `main.py` at line 57, replacing the existing `music.play(...)` call, then re-upload.

---

## Backing up / restoring the original firmware

If the micro:bit had existing firmware you want to preserve, back it up first:

```bash
# Install pyocd
pip install pyocd

# Dump flash to file
pyocd cmd -c "savemem 0x0 0x80000 ~/microbit-backup.bin" -t nrf52833

# Convert to hex for easy restore
python3 -c "
from intelhex import IntelHex
ih = IntelHex()
ih.loadbin('microbit-backup.bin', offset=0x0)
ih.write_hex_file('microbit-backup.hex')
"
```

To restore: copy `microbit-backup.hex` to the `MICROBIT` USB drive.
