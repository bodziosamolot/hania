import board
import neopixel_spi as neopixel
import time
import math
import random

spi = board.SPI()
num_pixels = 12
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel_SPI(
    spi, num_pixels, brightness=0.3, auto_write=False, pixel_order=ORDER,
    bit0=0b10000000, bit1=0b11111100, frequency=6400000
)


def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)


def scale(color, factor):
    return tuple(max(0, min(255, int(c * factor))) for c in color)


def blend(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def breathing(color, cycles=3, steps=80):
    for _ in range(cycles):
        for s in range(steps):
            brightness = (math.sin(s / steps * math.pi * 2 - math.pi / 2) + 1) / 2
            pixels.fill(scale(color, brightness))
            pixels.show()
            time.sleep(0.025)


def comet(color, cycles=4, tail_length=5):
    for _ in range(cycles):
        for head in range(num_pixels * 2):
            pixels.fill((0, 0, 0))
            for t in range(tail_length):
                idx = (head - t) % num_pixels
                fade = 1.0 - (t / tail_length)
                pixels[idx] = scale(color, fade ** 2)
            pixels.show()
            time.sleep(0.05)


def rainbow_comet(cycles=4, tail_length=6):
    for _ in range(cycles):
        for head in range(num_pixels * 2):
            pixels.fill((0, 0, 0))
            for t in range(tail_length):
                idx = (head - t) % num_pixels
                hue = ((head - t) * 256 // num_pixels) % 256
                fade = 1.0 - (t / tail_length)
                pixels[idx] = scale(wheel(hue), fade ** 1.5)
            pixels.show()
            time.sleep(0.05)


def fire(duration=6):
    heat = [0] * num_pixels
    start = time.time()
    while time.time() - start < duration:
        for i in range(num_pixels):
            heat[i] = max(0, heat[i] - random.randint(0, 20))
        for i in range(num_pixels - 1, 1, -1):
            heat[i] = (heat[i - 1] + heat[i - 2]) // 3
        if random.random() < 0.6:
            idx = random.randint(0, 2)
            heat[idx] = min(255, heat[idx] + random.randint(160, 255))
        for i in range(num_pixels):
            h = heat[i]
            if h < 85:
                pixels[i] = (h * 3, 0, 0)
            elif h < 170:
                pixels[i] = (255, (h - 85) * 3, 0)
            else:
                pixels[i] = (255, 255, min(255, (h - 170) * 4))
        pixels.show()
        time.sleep(0.03)


def sparkle(color, duration=5, density=0.15):
    start = time.time()
    while time.time() - start < duration:
        pixels.fill((0, 0, 0))
        for i in range(num_pixels):
            if random.random() < density:
                bright = random.uniform(0.3, 1.0)
                pixels[i] = scale(color, bright)
        pixels.show()
        time.sleep(0.06)


def rainbow_sparkle(duration=5, density=0.25):
    start = time.time()
    while time.time() - start < duration:
        pixels.fill((0, 0, 0))
        for i in range(num_pixels):
            if random.random() < density:
                pixels[i] = wheel(random.randint(0, 255))
        pixels.show()
        time.sleep(0.06)


def theater_chase_rainbow(cycles=8):
    for j in range(256 * cycles // num_pixels):
        for q in range(3):
            pixels.fill((0, 0, 0))
            for i in range(0, num_pixels, 3):
                idx = i + q
                if idx < num_pixels:
                    pixels[idx] = wheel((idx * 256 // num_pixels + j * 3) % 256)
            pixels.show()
            time.sleep(0.06)


def larson_scanner(color, cycles=4, width=3):
    for _ in range(cycles):
        for direction in (range(num_pixels), range(num_pixels - 1, -1, -1)):
            for pos in direction:
                pixels.fill((0, 0, 0))
                for w in range(-width, width + 1):
                    idx = pos + w
                    if 0 <= idx < num_pixels:
                        fade = 1.0 - abs(w) / (width + 1)
                        pixels[idx] = scale(color, fade ** 2)
                pixels.show()
                time.sleep(0.04)


def plasma(duration=8):
    start = time.time()
    t = 0
    while time.time() - start < duration:
        for i in range(num_pixels):
            angle = i / num_pixels * math.pi * 2
            v1 = math.sin(angle + t * 1.5)
            v2 = math.sin(angle * 2 - t * 0.8)
            v3 = math.sin(angle + t * 2.2 + math.pi / 3)
            val = (v1 + v2 + v3) / 3.0
            hue = int((val + 1) / 2 * 255) % 256
            pixels[i] = wheel(hue)
        pixels.show()
        t += 0.15
        time.sleep(0.03)


def color_wave(duration=8):
    start = time.time()
    offset = 0.0
    while time.time() - start < duration:
        for i in range(num_pixels):
            wave = (math.sin(offset + i * math.pi * 2 / num_pixels) + 1) / 2
            hue = int((i / num_pixels * 256 + offset * 40) % 256)
            pixels[i] = scale(wheel(hue), wave)
        pixels.show()
        offset += 0.12
        time.sleep(0.03)


def pulse_ring(cycles=3):
    colors = [(255, 0, 50), (0, 200, 255), (100, 255, 0)]
    for color in colors:
        for step in range(num_pixels + 4):
            pixels.fill((0, 0, 0))
            for i in range(num_pixels):
                dist = abs(i - step)
                if dist < 3:
                    pixels[i] = scale(color, max(0, 1 - dist / 3))
            pixels.show()
            time.sleep(0.04)
        for step in range(num_pixels + 4, -1, -1):
            pixels.fill((0, 0, 0))
            for i in range(num_pixels):
                dist = abs(i - step)
                if dist < 3:
                    pixels[i] = scale(color, max(0, 1 - dist / 3))
            pixels.show()
            time.sleep(0.04)


def dual_comets(cycles=5):
    tail = 4
    for _ in range(cycles):
        for step in range(num_pixels):
            pixels.fill((0, 0, 0))
            for t in range(tail):
                i1 = (step - t) % num_pixels
                i2 = (num_pixels - 1 - step + t) % num_pixels
                fade = (1.0 - t / tail) ** 2
                pixels[i1] = scale((0, 150, 255), fade)
                c2 = scale((255, 80, 0), fade)
                existing = pixels[i2]
                pixels[i2] = tuple(min(255, existing[c] + c2[c]) for c in range(3))
            pixels.show()
            time.sleep(0.06)


try:
    print("=== Breathing Cyan ===")
    breathing((0, 255, 200), cycles=3)

    print("=== Comet ===")
    comet((0, 150, 255), cycles=4)

    print("=== Rainbow Comet ===")
    rainbow_comet(cycles=4)

    print("=== Fire ===")
    fire(duration=6)

    print("=== Sparkle ===")
    sparkle((255, 255, 255), duration=4)

    print("=== Rainbow Sparkle ===")
    rainbow_sparkle(duration=4)

    print("=== Theater Chase Rainbow ===")
    theater_chase_rainbow(cycles=6)

    print("=== Larson Scanner ===")
    larson_scanner((255, 0, 0), cycles=3)

    print("=== Plasma ===")
    plasma(duration=8)

    print("=== Color Wave ===")
    color_wave(duration=8)

    print("=== Pulse Ring ===")
    pulse_ring(cycles=2)

    print("=== Dual Comets ===")
    dual_comets(cycles=6)

finally:
    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(0.1)
    pixels.deinit()
