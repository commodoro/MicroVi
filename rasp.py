from sys import stderr

try:
    import gpiozero
    class Light:
        PIN_LED = 17
        def __init__(self):
            self.pwm = gpiozero.PWMLED(self.PIN_LED, frequency=1000)
        
        def level(self, lv: float):
            self.pwm.value = 1-float(lv)

        def turn_off(self):
            self.pwm.off()

        def turn_on(self):
            self.pwm.on()
except ImportError:
    print('Raspberry required for run', file=stderr)
    class Light:        
        def level(self, lv: float):
            print("Light Level:", lv)

        def turn_off(self):
            print("Light Off")

        def turn_on(self):
            print("Light On")
