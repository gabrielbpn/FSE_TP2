import RPi.GPIO as GPIO

class Forno:
    def __init__(self):
        porta_r = 23
        porta_v = 24

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(porta_r, GPIO.OUT)
        GPIO.setup(porta_v, GPIO.OUT)

        self.resistor = GPIO.PWM(porta_r, 1000)
        self.resistor.start(0)

        self.ventoinha = GPIO.PWM(porta_v, 1000)
        self.ventoinha.start(0)

    def aquecer(self, pid):
        self.resistor.ChangeDutyCycle(pid)

    def resfriar(self, pid):
        self.ventoinha.ChangeDutyCycle(pid)
