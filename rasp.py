from sys import stderr

try:
    import serial
    class Light:
        lv : int = 0
        def __init__(self):
            self.uart = serial.Serial('/dev/ttyAMA0', 9600)
        
        def level(self, lv: int):
            print("Nivel: ", lv, bytes((self.lv,)))
            self.lv = int(lv)
            self.uart.write(bytes((self.lv,)))

        def turn_off(self):
            self.uart.write(b'\x00')

        def turn_on(self):
            self.uart.write(bytes((self.lv,)))
except ImportError:
    print('Raspberry required for run', file=stderr)
    class Light:        
        def level(self, lv: float):
            print("Light Level:", lv)

        def turn_off(self):
            print("Light Off")

        def turn_on(self):
            print("Light On")
