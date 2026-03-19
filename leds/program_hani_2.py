import board
import neopixel_spi as neopixel
import time
import random

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

# -------------------------------------------------

# (0, 200, 100),     # Teal
poprzedni_pixel_1 = -1
poprzedni_pixel_2 = -1

for lap in range(100):

    aktualny_pixel_1 = random.randint(0,11)
    aktualny_pixel_2 = random.randint(0,11)
    
    pixels[poprzedni_pixel_1] = (0,0,0)
    pixels[poprzedni_pixel_2] = (0,0,0)
    pixels[aktualny_pixel_1] = (random.randint(0,255), 0, 150)
    pixels[aktualny_pixel_2] = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    pixels.show()
    time.sleep(0.04)
    
    poprzedni_pixel_1 = aktualny_pixel_1
    poprzedni_pixel_2 = aktualny_pixel_2
    

# -------------------------------------------------

# Turn off all pixels and release the SPI bus
pixels.fill((0, 0, 0))
pixels.show()
time.sleep(0.1)
pixels.deinit()
