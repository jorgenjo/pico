# Oled Display Driver
# SSD1362
# Tested on MDOB256064D1Y

import framebuf
import time


class SSD1362(framebuf.FrameBuffer):

    def __init__(self, width, height, spi, dc, res, cs):
        self.width = width
        self.height = height
        self.spi = spi
        self.dc = dc
        self.res = res
        self.cs = cs
        self.rate = 10 * 1024 * 1024  # 10 MHz SPI speed

        # Initialize SPI pins
        self.dc.init(self.dc.OUT, value=0)
        self.res.init(self.res.OUT, value=0)
        self.cs.init(self.cs.OUT, value=1)

        # Reset and initialize display
        self.reset()
        self.init_display()

        # Use 4-bit grayscale buffer
        buffer_size = width * height // 2  # 4-bit = 2 pixels per byte
        self.buffer = bytearray(buffer_size)

        super().__init__(self.buffer, width, height, framebuf.GS4_HMSB)

    # Is overwritten by subcæass
    def write_cmd(self, cmd):
        raise NotImplementedError("write_cmd() must be implemented in a subclass.")

    # Is overwritten by subcæass
    def write_data(self, buf):
        raise NotImplementedError("write_data() must be implemented in a subclass.")
    



    def init_display(self):
        """Initialize SSD1362 display with correct orientation."""
        cmds = [
            0xFD, 0x12,  # Set COmmand Lock  12=Unlock 16=Lock

            0xAE,  # Display OFF (sleepmode)

            0x15,  # Set Column Adress
            0x00,  
            0x7F,  

            0x75,  # Set Column Adress
            0x00,  
            0x3F,  

            0x81,  # Set Contrasts
            0x2F,  

            0xA0,  # Set Remap
            0xC3,  

            0xA1,  # Set Display Start Line
            0x00,  

            0xA2,  # Set Display Offset
            0x00,  

            0xA4,  # Normal Display

            0xA8,  # Set Multiplex Ratio
            0x3F,  

            0xAB,  # VDD Regulator
            0x01,  # Regulator Enable  

            0xAD,  # External Internal IREF Selection
            0x8E,    

            0xB1,  # Set Phase Length
            0x22,    

            0xB3,  # Display Clock Divider
            0xA0,  # A0 = 90 Hz, # F0 = 100 Hz,

            0xB6,  # Set Second pre-charge Period
            0x04,    

            0xB9,  # Set Linear LUTSecond pre-charge Period

            0xBC,  # Set Pre charg voltage levelSecond pre-charge Period
            0x10,  # 0.5*Vcc    

            0xBD,  # Set Pre charg voltage capacitor slection
            0x01,      

            0xAF  # Display ON

        ]
        for cmd in cmds:
            self.write_cmd(cmd)


    def fill(self, grayscale_value):
        """Fill screen with a specific grayscale value (0x0 to 0xF)."""
        grayscale_value &= 0xF  # Ensure it's within 4-bit range
        byte_value = (grayscale_value << 4) | grayscale_value  # Pack two pixels per byte
        self.buffer[:] = bytes([byte_value] * len(self.buffer))

    
    def pixel(self, x, y, grayscale_value):
        """Set a pixel at (x, y) with a 4-bit grayscale value."""
        index = (y * self.width + x) // 2
        if x % 2 == 0:
            self.buffer[index] = (self.buffer[index] & 0x0F) | (grayscale_value << 4)
        else:
            self.buffer[index] = (self.buffer[index] & 0xF0) | (grayscale_value & 0x0F)


    def reset(self):
        """Resets the display."""
        self.res(1)
        time.sleep_ms(1)
        self.res(0)
        time.sleep_ms(10)
        self.res(1)


class SSD1362_SPI(SSD1362):
    def __init__(self, width, height, spi, dc, res, cs):
        self.width = width
        self.height = height
        self.rate = 10 * 1024 * 1024  # 10 MHz SPI speed
        self.spi = spi
        self.dc = dc
        self.res = res
        self.cs = cs
        
        # Initialize SPI pins
        self.dc.init(self.dc.OUT, value=0)
        self.res.init(self.res.OUT, value=0)
        self.cs.init(self.cs.OUT, value=1)

        # Clear the buffer
        self.buffer = bytearray(width * height // 2)  # 4-bit grayscale

        super().__init__(width, height, spi, dc, res, cs)


    def write_cmd(self, cmd):
        """Sends a command to the display."""
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs(1)
        self.dc(0)  # Command mode
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        """Sends data to the display."""
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs(1)
        self.dc(1)  # Data mode
        self.cs(0)
        self.spi.write(buf)
        self.cs(1)


    def show(self):
        """Sends the buffer to the display."""
        self.write_cmd(0x15)  # Set Column Address
        self.write_cmd(0x00)
        self.write_cmd(0xFF)

        self.write_cmd(0x75)  # Set Row Address
        self.write_cmd(0x00)
        self.write_cmd(0x3F)

        self.write_data(self.buffer)
        self.write_cmd(0xA4)  # Write RAM Command


    def clear(self):
        """Clears the display buffer."""
        self.buffer = bytearray(self.width * self.height // 2)
        self.show()



