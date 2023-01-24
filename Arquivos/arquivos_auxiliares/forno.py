import RPi.GPIO as GPIO

class Forno:
    def __init__(self):
        portaResistor = 23
        portaVentoinha = 24
    
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(portaResistor, GPIO.OUT)
        GPIO.setup(portaVentoinha, GPIO.OUT)

        self.resistor = GPIO.PWM(portaResistor, 60)
        self.resistor.start(0)

        self.ventoinha = GPIO.PWM(portaVentoinha, 60)
        self.ventoinha.start(0)

    def aquecer(self, pid):
        self.resistor.ChangeDutyCycle(pid)

    def resfriar(self, pid):
        self.ventoinha.ChangeDutyCycle(pid)
