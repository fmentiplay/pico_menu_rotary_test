"""
Exercise on Raspberry Pi Pico/MicroPython
with 320x240 ILI9341 SPI Display
"""
from ili934xnew import ILI9341, color565
from machine import Pin, SPI
from micropython import const
import glcdfont
import tt14
import tt24
import tt32
import time

SCR_WIDTH = const(320)
SCR_HEIGHT = const(240)
SCR_ROT = const(2)
CENTER_Y = int(SCR_WIDTH/2)
CENTER_X = int(SCR_HEIGHT/2)

TFT_CLK_PIN = const(2)
TFT_MOSI_PIN = const(3)
TFT_MISO_PIN = const(4)

TFT_CS_PIN = const(5)
TFT_RST_PIN = const(0)
TFT_DC_PIN = const(1)

dt = 17  # dt connected to GP17, step pin pin
clk = 16 # clk connected to GP16, direction pin

dt_pin = Pin(dt, Pin.IN)  # Using 10K Pullup resistor on Rotary encoder dev board
clk_pin = Pin(clk, Pin.IN)  # Using 10K Pullup resistor on Rotary encoder dev board

# fonts = [glcdfont,tt14,tt24,tt32]

spi = SPI(
    0,
    baudrate=40000000,
    miso=Pin(TFT_MISO_PIN),
    mosi=Pin(TFT_MOSI_PIN),
    sck=Pin(TFT_CLK_PIN))

display = ILI9341(
    spi,
    cs=Pin(TFT_CS_PIN),
    dc=Pin(TFT_DC_PIN),
    rst=Pin(TFT_RST_PIN),
    w=SCR_WIDTH,
    h=SCR_HEIGHT,
    r=SCR_ROT)

display.erase()
display.fill_rectangle(0, 0, 240, 320, color=color565(0,0,0))    

def menu_item(c1, c2, c3, x, y, font, Text):
    display.set_pos(x, y)
    display.set_font(font)
    display.set_color(color565(c1, c2, c3), color565(0, 0, 0))
    display.print(Text)

def display_main():    
    menu_item(255, 0, 0, 45, 20, tt32, 'Main Menu')
    menu_item(0, 255, 0, 45, 60, tt24, 'SubMenu 1')
    menu_item(0, 255, 0, 45, 100, tt24, 'SubMenu 2')
    menu_item(0, 255, 0, 45, 140, tt24, 'SubMenu 3')
    
def display_SubMenu1():    
    menu_item(0, 255, 0, 45, 20, tt32, 'SubMenu 1')
    menu_item(0, 255, 0, 45, 60, tt24, 'Item 1')
    menu_item(0, 255, 0, 45, 100, tt24, 'Item 2')
    menu_item(0, 255, 0, 45, 140, tt24, 'Item 3')
# time.sleep(1)

display_main()

print("- bye-")



# from machine import Pin
# from time import sleep

sw = Pin(18, Pin.IN, Pin.PULL_UP)

switch_state = False  # switch in open position, GP26 high

def handle_interrupt(pin):
    global switch_state
    switch_state = True    # switch closed, GP26 low
    
def clk_pin_interrupt(pin):
    global a
    global b
    a = clk_pin.value()
    b = dt_pin.value()
    # print("clk_pin = ", a)
    # print("dt_pin = ", b)
    global change
    change = True
    
sw.irq(trigger=Pin.IRQ_FALLING, handler=handle_interrupt)  # interrupt triggered when switch is pressed (closed)
clk_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=clk_pin_interrupt)

#previous_value = clk_pin.value()
change = False
state = 0 # Main Menu with text "Main Menu" highlighted

while True:
    if switch_state:
        # print('Switch Pressed, Interrupt caused by: ', sw)
         #menu_item(255,0, 0, 45, 100, tt32, "SubMenu 2")
        if state == 0:
            print("You are at Main Menu")
        # sleep(1)
        switch_state = False
        
    # if previous_value != clk_pin.value():
    if change:   # implied change = True
        if ((a != b) and state == 0):
            menu_item(0, 255, 0, 45, 20, tt32, 'Main Menu')
            menu_item(255, 0, 0, 45, 60, tt24, 'SubMenu 1')
            state = 1 # Main Menu with text "SubMenu 1" highlighted
            # print("state = ", state)
        elif ((a == b) and state == 0):
            menu_item(0, 255, 0, 45, 20, tt32, 'Main Menu')
            menu_item(255, 0, 0, 45, 140, tt24, 'SubMenu 3')
            state = 3
        elif ((a != b) and state == 1):
            menu_item(0, 255, 0, 45, 60, tt24, 'SubMenu 1')
            menu_item(255, 0, 0, 45, 100, tt24, 'SubMenu 2')
            state = 2      # Main Menu with text "SubMenu 1" highlighted
            # print("state = ", state)
        elif ((a == b) and state == 1):
            #pass
            menu_item(0, 255, 0, 45, 60, tt24, 'SubMenu 1')
            menu_item(255, 0, 0, 45, 20, tt32, 'Main Menu')
            state = 0
        elif ((a != b) and state == 2):
            menu_item(0, 255, 0, 45, 100, tt24, 'SubMenu 2')
            menu_item(255, 0, 0, 45, 140, tt24, 'SubMenu 3')
            state = 3     # Main Menu with text "SubMenu 1" highlighted
            # print("state = ", state)
        elif ((a == b) and state == 2):
            #pass
            menu_item(0, 255, 0, 45, 100, tt24, 'SubMenu 2')
            menu_item(255, 0, 0, 45, 60, tt24, 'SubMenu 1')
            state = 1
        elif ((a != b) and state == 3):
            menu_item(0, 255, 0, 45, 140, tt24, 'SubMenu 3')
            menu_item(255, 0, 0, 45, 20, tt32, 'Main Menu')
            state = 0     # Main Menu with text "SubMenu 1" highlighted
            # print("state = ", state)
        elif ((a == b) and state == 3):
            #pass
            menu_item(0, 255, 0, 45, 140, tt24, 'SubMenu 3')
            menu_item(255, 0, 0, 45, 100, tt24, 'SubMenu 2')
            state = 2
        else:
            # pass
            print("At else statement")
            print("state = ", state)
            
                       
        # previous_value = clk_pin.value()
        change = False
        
    time.sleep(0.1)
    #print("charge = ", change)
        # print(clk_pin.value())
    #print(state)
        # time.sleep(1)
        
"""

while True:
    pass
"""