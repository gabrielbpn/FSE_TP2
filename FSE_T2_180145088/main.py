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
from arquivos_auxiliares.csv import CSV

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

    iniciandoAquecimento = 0

    def __init__(self):
        self.usuarioComando()
        self.menu()
        self.csv = CSV()

    def menu(self):
        while(1):
            time.sleep(3)
            self.usuarioComando()
            tempInt = self.solicitarTemperaturaInt()
            tempRef = self.solicitarTemperaturaRef()

            if self.estadoAtual == 161: # transformei 0xa1 pra decimal
                self.ligarForno()

            elif self.estadoAtual == 162:
                self.desligarForno()

            elif self.estadoAtual == 163:
                self.ligarAquecimento()
                self.iniciandoAquecimento = 1

            elif self.estadoAtual == 164:
                self.desligarAquecimento()
                self.iniciandoAquecimento = 0

            elif self.iniciandoAquecimento == 1:
                #self.pid.pidAtualizaReferencia(tempRef)
                comandoEstado = b'\x01\x23\xd1'
                controlaPid = self.pid.controlePid(tempRef, tempInt)
                valorPid = int(controlaPid).to_bytes(4, 'little', signed=True)
                self.uart.envia(comandoEstado, self.matricula, valorPid, 11)
                self.fornoFuncionamento()

            else:
                pass


    def usuarioComando(self):
            self.response = 0
            self.uart.envia(b'\x01\x23\xc3', self.matricula, b'',  7) # le o comando do usuario
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

    def desligarAquecimento(self):
        comandoEstado = b'\x01\x23\xd3'
        self.uart.envia(comandoEstado, self.matricula, b'\x00', 8)

        dados = self.uart.recebe()
        
        if dados is not None:
            print("Aquecimento desligado")

    def salva_log(self):
        header = ['data', 'ti', 'tr', 'resistor/ventoinha']
        self.csv.escrever(header)
        
        while True:
            dado = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            linha = [dado, self.tempInterna, self.tempRef, self.pid.controleMin]
            self.csv.escrever(linha)
            time.sleep(1)

    def fornoFuncionamento(self):
        pidAuxiliar = self.pid.controlePid(self.tempRef, self.tempInterna)  

        print(self.tempInterna)
        if pidAuxiliar < 0:
            pidAuxiliar *= -1

        if (pidAuxiliar < 40): # Forno frio
            print("Tá muito quente!")
            pidAuxiliar = 40
            self.forno.resfriar(pidAuxiliar)

        else: 
            print("Tá frio demais!") # Forno quente
            print(pidAuxiliar)
            self.forno.aquecer(pidAuxiliar)

        time.sleep(2)
    
    def solicitarTemperaturaInt(self):
        comandoEstado = b'\x01\x23\xc1'
        self.uart.envia(comandoEstado, self.matricula, b'', 7)
        
        dados = self.uart.recebe()

        temp = [dados[0], dados[1], dados[2], dados[3]] 
        temperatura = struct.unpack('f', bytearray(temp))[0]

        print('\nTemperatura interna:', temperatura)
        print("")
        
        return temperatura

    def solicitarTemperaturaRef(self):
        comandoEstado = b'\x01\x23\xc2'
        self.uart.envia(comandoEstado, self.matricula, b'', 7)
        dados = self.uart.recebe()

        temp = [dados[0], dados[1], dados[2], dados[3]] 
        temperatura = struct.unpack('f', bytearray(temp))[0]

        print('\nTemperatura Referência:', temperatura)
        print("")

        return temperatura

if __name__ == '__main__':
    Main()