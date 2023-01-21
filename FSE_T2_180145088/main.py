import serial
import time
import datetime
import struct
import math

from threading import Event, Thread 

from UART import UART
from PID import PID
from forno import Forno

class Forno:
    port = '/dev/serial0'
    baudrate = 9600
    timeout = 0.5
    matricula = [5, 0, 8, 8]
