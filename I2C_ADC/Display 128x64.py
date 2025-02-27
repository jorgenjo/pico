from machine import Pin, I2C
import ssd1306

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)


oled.fill(0x00)
# Font 8x8

oled.text("Val Controls IDC24",0,0,0xF)
oled.text("Val Controls IDC24",0,8,0xF)
oled.text("Val Controls IDC24",0,16,0xF)
oled.text("Val Controls IDC24",0,24,0xF)


oled.show()