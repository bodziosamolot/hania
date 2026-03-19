"""Test program for verifying HC-SR04 ultrasonic sensor on Raspberry Pi 5."""

import time
import sys

from gpiozero import DistanceSensor
from gpiozero.exc import GPIOZeroError


TRIGGER_PIN = 23
ECHO_PIN = 24
MAX_DISTANCE_M = 4.0
MEASUREMENT_INTERVAL_S = 1.0


def create_sensor(
    trigger: int, echo: int, max_distance: float
) -> DistanceSensor:
    """Create and return a DistanceSensor instance.

    Parameters:
        trigger (int): GPIO pin number for TRIGGER.
        echo (int): GPIO pin number for ECHO.
        max_distance (float): Maximum measurable distance in meters.

    Returns:
        DistanceSensor: Configured sensor object.
    """
    return DistanceSensor(
        echo=echo, trigger=trigger, max_distance=max_distance
    )


def read_distance(sensor: DistanceSensor) -> float:
    """Read distance from the sensor in centimeters.

    Parameters:
        sensor (DistanceSensor): The distance sensor instance.

    Returns:
        float: Measured distance in centimeters.
    """
    return sensor.distance * 100


def main() -> None:
    """Run continuous distance measurements and print results."""
    print(
        f"HC-SR04 Test — TRIGGER=GPIO{TRIGGER_PIN}, "
        f"ECHO=GPIO{ECHO_PIN}"
    )
    print("Press Ctrl+C to stop.\n")

    try:
        sensor = create_sensor(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE_M)
    except GPIOZeroError as exc:
        print(f"Failed to initialise sensor: {exc}")
        sys.exit(1)

    try:
        while True:
            distance_cm = read_distance(sensor)
            print(f"Distance: {distance_cm:6.1f} cm")
            time.sleep(MEASUREMENT_INTERVAL_S)
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        sensor.close()


if __name__ == "__main__":
    main()
