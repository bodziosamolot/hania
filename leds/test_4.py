import board
import neopixel_spi as neopixel

spi = board.SPI()
pixels = neopixel.NeoPixel_SPI(
    spi, 12, brightness=0.3, auto_write=True, pixel_order=neopixel.GRB,
    bit0=0b10000000, bit1=0b11111100, frequency=6400000
)
pixels.fill((255, 0, 0))