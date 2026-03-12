# Leprechaun Trap

micro:bit V2 project: sonar-triggered servo trap with animated LED display and sound.

## Hardware

- BBC micro:bit V2
- HC-SR04 sonar sensor (trigger: P14, echo: P13)
- Servo motor (P1)
- 2x AAA batteries

## How it works

- Idles with display off, polling sonar every 500ms
- When something enters ~25cm range, display wakes and shows distance in cm
- When something comes within 5cm, plays a melody, actuates the servo, then animates a shrinking countdown on the LED grid
- Resets after ~3.5 seconds, 2 second cooldown before re-arming

## Config (top of main.py)

| Variable | Default | Description |
|---|---|---|
| `START_ANGLE` | 36 | Servo resting position |
| `CAPTURE_ANGLE` | 55 | Servo trigger position |
| `TRIGGER_CM` | 5 | Trigger distance (cm) |
| `WAKE_CM` | 25 | Wake-from-idle distance (cm) |
| `RESET_MS` | 3500 | Time before servo resets (ms) |

## Flashing

Requires MicroPython firmware on the micro:bit. Upload `main.py` via [microfs](https://github.com/ntoll/microfs):

```bash
pip install microfs
ufs put main.py
```

Then soft-reset via serial (Ctrl+D) or press the reset button.

## Melodies

Open `melodies.html` in a browser to preview and pick a trigger melody.
