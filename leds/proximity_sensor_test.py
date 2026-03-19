import time
import sys

from gpiozero import DistanceSensor
from gpiozero.exc import GPIOZeroError

import board
import neopixel_spi as neopixel


TRIGGER_PIN = 23
ECHO_PIN = 24
MAX_DISTANCE_M = 4.0
MEASUREMENT_INTERVAL_S = 0.05

NUM_PIXELS = 12
NUM_LEVELS = NUM_PIXELS // 2

MAX_RANGE_CM = 30.0
MIN_RANGE_CM = 2.0

LEVEL_COLORS = [
    (0, 0, 255),
    (0, 100, 255),
    (0, 255, 200),
    (100, 255, 0),
    (255, 255, 0),
    (255, 0, 0),
]

LED_PAIRS = [(0, 11), (1, 10), (2, 9), (3, 8), (4, 7), (5, 6)]


def create_sensor(trigger: int, echo: int, max_distance: float) -> DistanceSensor:
    return DistanceSensor(echo=echo, trigger=trigger, max_distance=max_distance)


def read_distance(sensor: DistanceSensor) -> float:
    return sensor.distance * 100


def distance_to_level(distance_cm: float) -> int:
    clamped = max(MIN_RANGE_CM, min(MAX_RANGE_CM, distance_cm))
    ratio = 1.0 - (clamped - MIN_RANGE_CM) / (MAX_RANGE_CM - MIN_RANGE_CM)
    return int(ratio * NUM_LEVELS)


def update_leds(pixels, level: int) -> None:
    pixels.fill((0, 0, 0))
    for i in range(level):
        left, right = LED_PAIRS[i]
        pixels[left] = LEVEL_COLORS[i]
        pixels[right] = LEVEL_COLORS[i]
    pixels.show()


def main() -> None:
    print(f"Proximity LED — TRIGGER=GPIO{TRIGGER_PIN}, ECHO=GPIO{ECHO_PIN}")
    print(f"Range: {MIN_RANGE_CM}–{MAX_RANGE_CM} cm, {NUM_LEVELS} levels")
    print("Press Ctrl+C to stop.\n")

    spi = board.SPI()
    pixels = neopixel.NeoPixel_SPI(
        spi, NUM_PIXELS, brightness=0.15, auto_write=False,
        pixel_order=neopixel.GRB,
        bit0=0b10000000, bit1=0b11111100, frequency=6400000,
    )

    try:
        sensor = create_sensor(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE_M)
    except GPIOZeroError as exc:
        print(f"Failed to initialise sensor: {exc}")
        sys.exit(1)

    prev_level = -1
    try:
        while True:
            distance_cm = read_distance(sensor)
            level = distance_to_level(distance_cm)

            if level != prev_level:
                update_leds(pixels, level)
                prev_level = level

            print(f"Distance: {distance_cm:5.1f} cm  |  Level: {level}/{NUM_LEVELS}")
            time.sleep(MEASUREMENT_INTERVAL_S)

    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        pixels.fill((0, 0, 0))
        pixels.show()
        pixels.deinit()
        sensor.close()


if __name__ == "__main__":
    main()
