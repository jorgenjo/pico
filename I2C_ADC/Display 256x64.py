from machine import Pin, I2C, SPI
#import ssd1306
import ssd1362

#i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
#oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)


spi = SPI(1, baudrate=5000000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11))
dc = Pin(8)  # Data/Command pin
res = Pin(12)  # Reset pin
cs = Pin(9)  # Chip Select pin
oled = ssd1362.SSD1362_SPI(256, 64, spi, dc, res, cs)


#oled.fill(0xFF)
oled.fill(0x00)
# Font 8x8

oled.text("Val Controls IDC24",0,0,0xF)
oled.text("Val Controls IDC24",0,8,0xF)
oled.text("Val Controls IDC24",0,16,0xF)
oled.text("Val Controls IDC24",0,24,0xF)


oled.show()

