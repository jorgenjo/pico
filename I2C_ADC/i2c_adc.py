"""
MicroPython script for Raspberry Pi Pico W (Pico2 W)
-----------------------------------------------------
This script communicates with an INA226 power monitor over I2C using the Raspberry Pi Pico W.
It reads bus voltage, current, and power measurements via I2C and prints them to the console.

Hardware:
- Raspberry Pi Pico W (Pico2 W)
- INA226 power monitor sensor
- I2C connection using GPIO0 (SDA) and GPIO1 (SCL)

MicroPython Dependencies:
- machine (for Pin, I2C)
- time (for delays)

Author: [Jørgen Johannessen]
Date: [2025-02-10]
"""



from machine import Pin, I2C
import ssd1306

import time

# INA226 I2C address (default is 0x40, but may be 0x41, 0x42, etc.)
INA226_I2C_ADDR = 0x40

# INA226 Register Addresses
REG_VOLTAGE  = 0x02  # Bus Voltage Register
REG_CURRENT  = 0x01  # Current Register
REG_POWER    = 0x03  # Power Register

# Initialize I2C on GPIO0 (SDA) and GPIO1 (SCL)
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)

# Function to read a 16-bit register from INA226
def read_register(reg):
    data = i2c.readfrom_mem(INA226_I2C_ADDR, reg, 2)  # Read 2 bytes
    return (data[0] << 8) | data[1]  # Convert to 16-bit value

while True:
    try:
        # Read values from INA226
        voltage_raw = read_register(REG_VOLTAGE)
        current_raw = read_register(REG_CURRENT)
        power_raw = read_register(REG_POWER)

        # Convert raw values to actual measurements
        bus_voltage = voltage_raw * 1.25 / 1000  # 1.25mV per bit, convert to Volts
        current = current_raw * 1.25 / 1000  # Scale current based on calibration (assumes default)
        power = power_raw * 25 / 1000  # 25mW per bit, convert to Watts

        #print(f"Bus Voltage: {bus_voltage:.3f} V")
        print(f"Current: {current:.2f} mA")
        #print(f"Power: {power:.3f} W")
        print("------------------------")

    except Exception as e:
        print("I2C Read Error:", e)

    time.sleep(1)  # Delay before next read
