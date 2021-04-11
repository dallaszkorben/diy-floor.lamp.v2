

Fetch micropython-rotary project:
    git clone https://github.com/miketeachman/micropython-rotary.git

Upload project to ESP2866:
    ampy -p /dev/ttyUSB0 -b 115200 put rotary.py
    ampy -p /dev/ttyUSB0 -b 115200 put rotary_irq_esp.py
    ampy -p /dev/ttyUSB0 -b 115200 put start.py

