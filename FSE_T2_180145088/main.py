import serial
import time
import datetime
import struct
import math

from threading import Event, Thread 

from arquivos_auxiliares.UART import UART
from arquivos_auxiliares.PID import PID
from arquivos_auxiliares.forno import Forno
from arquivos_auxiliares.crc import calcula_CRC

class Main():
    port =  '/dev/serial0'
    baudrate = 9600
    timeout = 0.5   
    matricula = b'\x05\x00\x08\x08'

    uart = UART(port, baudrate, timeout)
    pid = PID()
    forno = Forno()

    tempRef = 0
    tempInterna = 0
    estadoAtual = 0
    tempSala = 0

    def __init__(self):
        self.menu()

    def menu(self):
        while(1):
            time.sleep(3)

            if self.estadoAtual == 161: # transformei 0xa1 pra decimal
                self.ligarForno()

            elif self.estadoAtual == 162:
                self.desligarForno()

            elif self.estadoAtual == 163:
                self.ligarAquecimento()

            elif self.estadoAtual == 164:
                self.desligarAquecimento()

            else:
                pass

    def usuarioComando(self):
        self.response = 0
        self.uart.envia(b'\x01\x23\xc3\x05\x00\x08\x08' + b'',  7) # le o comando do usuario
        estadoAtual = self.uart.recebe() 
        self.estadoAtual = struct.unpack('i', estadoAtual)[0] 

        print("Comando foi o : ", self.estadoAtual)

    def ligarForno(self):
        comandoEstado = b'\x01\x23\xd3'
        self.uart.envia(comandoEstado, self.matricula, b'\x01', 8)
        dados = self.uart.recebe()
        
        if dados is not None:
            print("Forno ligado")

    def desligarForno(self):    
        comandoEstado = b'\x01\x23\xd3'
        self.uart.envia(comandoEstado, self.matricula, b'\x00', 8)
        dados = self.uart.recebe()
        
        if dados is not None:
            print("Forno desligado")

    def ligarAquecimento(self):
        comandoEstado = b'\x01\x23\xd5'
        self.uart.envia(comandoEstado, self.matricula, b'\x01', 8)  
        dados = self.uart.recebe()
        
        if dados is not None:
            print("Aquecimento ligado")

    def fornoFuncionamento(self):
        pidAuxiliar = self.pid.controlePid(self.tempRef, self.tempInterna)  

        if (abs(pidAuxiliar) < 40): # Forno quente
            print("Tá muito quente!!!!")
            pidAuxiliar = 40
            self.forno.resfriar(pidAuxiliar)

        else: 
            print("Tá frio demais!!") # Forno frio
            self.forno.aquecer(pidAuxiliar)

        time.sleep(2)

    def desligarAquecimento(self):
        comandoEstado = b'\x01\x23\xd3'
        #self.uart.envia(comandoEstado, self.matricula, b'\x00', 8)

    def trataTemperaturas(self, bytes):
        comandoEstado = b'\x01\x23\xc2'

        for _ in range (2):
            self.uart.envia(comandoEstado, self.matricula, )
            comandoEstado = b'\x01\x23\xc1'

if __name__ == '__main__':
    Main()