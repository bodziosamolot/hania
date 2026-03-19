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

# (0, 200, 100),     # Teal

number_of_laps = 8
num_pixels = len(pixels)*number_of_laps

for pixel in range(num_pixels):
    pixel_index = pixel % len(pixels)
    pixels[pixel_index - 1] = (0,0,0)
    if pixel_index % 2 == 0:
        pixels[pixel_index] = (0, 200, 100)     # Teal
    else:
        pixels[pixel_index]=(255, 0, 255)  
    pixels.show()
    time.sleep(0.03)
    

# -------------------------------------------------

# Turn off all pixels and release the SPI bus
pixels.fill((0, 0, 0))
pixels.show()
time.sleep(0.1)
pixels.deinit()
