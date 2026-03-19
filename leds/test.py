import board
import neopixel_spi as neopixel
import time

# Initialize SPI bus (uses GPIO 10 / MOSI for data)
spi = board.SPI()

# Number of LEDs on the ring
num_pixels = 12

# Color byte order — most WS2812 rings use GRB
ORDER = neopixel.GRB

# Create NeoPixel object over SPI
# brightness: 0.0 (off) to 1.0 (max)
# auto_write=False means you must call pixels.show() to send data
# bit0/bit1/frequency: SPI timing tuned for WS2812 on Raspberry Pi 5
pixels = neopixel.NeoPixel_SPI(
    spi, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER,
    bit0=0b10000000, bit1=0b11111100, frequency=6400000
)

# --- Addressing pixels ---

# Set ALL pixels to green using fill(). Colors are (Red, Green, Blue), 0-255 each.
pixels.fill((0, 255, 0))
pixels.show()
time.sleep(3)

# Set INDIVIDUAL pixels by index (0 to num_pixels-1).
# Pixel 0 is the one closest to the DIN pad.
pixels.fill((0, 0, 0))       # clear all first
pixels[0] = (255, 0, 0)      # pixel 0 = red
pixels[1] = (0, 255, 0)      # pixel 1 = green
pixels[2] = (0, 0, 255)      # pixel 2 = blue
pixels[5] = (255, 255, 0)    # pixel 5 = yellow
pixels[11] = (255, 0, 255)   # pixel 11 (last) = magenta
pixels.show()
time.sleep(5)

# You can also use slices to set a range of pixels at once
pixels.fill((0, 0, 0))
pixels[0:4] = [(255, 0, 0)] * 4    # pixels 0-3 = red
pixels[4:8] = [(0, 255, 0)] * 4    # pixels 4-7 = green
pixels[8:12] = [(0, 0, 255)] * 4   # pixels 8-11 = blue
pixels.show()
time.sleep(5)

# Turn off all pixels and release the SPI bus
pixels.fill((0, 0, 0))
pixels.show()
time.sleep(0.1)
pixels.deinit()
