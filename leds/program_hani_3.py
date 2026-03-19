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
    spi, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER,
    bit0=0b10000000, bit1=0b11111100, frequency=6400000
)

# -------------------------------------------------

rainbow_12 = [
    (255, 0, 0),       # Red
    (255, 64, 0),      # Red-Orange
    (255, 127, 0),     # Orange
    (255, 200, 0),     # Yellow-Orange
    (255, 255, 0),     # Yellow
    (0, 255, 0),       # Green
    (0, 200, 100),     # Teal
    (0, 100, 255),     # Sky Blue
    (0, 0, 255),       # Blue
    (75, 0, 130),      # Indigo
    (148, 0, 211),     # Violet
    (200, 0, 150),     # Pink-Violet
]

number_of_laps = 2
number_of_pixels = len(pixels)*number_of_laps
tail_length = 11

for pixel in range(number_of_pixels):
    pixel = pixel % len(pixels)
    pixels[pixel - tail_length-1] = (0,0,0)
    
    for tail_index in range(tail_length):
        pixels[pixel-tail_index] = rainbow_12[tail_index]
        
    # pixels[pixel - 4] = (0,0,0)
    # pixels[pixel - 3] = (0,0,255)
    # pixels[pixel - 2] = (255,200,0)
    # pixels[pixel - 1] = (0,255,0)
    # pixels[pixel] = (200,0,150) # fioletowo rozowy
    pixels.show()
    time.sleep(0.2)

# -------------------------------------------------

# Turn off all pixels and release the SPI bus
pixels.fill((0, 0, 0))
pixels.show()
time.sleep(0.1)
pixels.deinit()
