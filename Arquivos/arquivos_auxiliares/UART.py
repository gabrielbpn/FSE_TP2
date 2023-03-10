import serial
import time

from arquivos_auxiliares.crc import calcula_CRC

class UART:
    conectado = False

    def __init__(self, port, baudrate, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.conecta()

    def conecta(self):
        self.serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)

        if (self.serial.isOpen()):
            self.conectado = True
            print('Porta aberta, conexao realizada')
        else:
            self.conectado = False
            print('Porta fechada, conexao nao realizada')
    
    def desconecta(self):
        self.serial.close()
        self.conectado = False
        print('Porta desconectada')

    def envia(self, comando, matricula, valor, tamanho):
        if (self.conectado):
            m1 = comando + bytes(matricula) + valor
            m2 = calcula_CRC(m1, tamanho).to_bytes(2, 'little')
            msg = m1 + m2
            self.serial.write(msg)
            #print('Mensagem enviada 1: {}'.format(msg))
        else:
            self.conecta()

    def recebe(self):
        if (self.conectado):
            time.sleep(0.2)
            buffer = self.serial.read(9)
            buffer_tam = len(buffer)

            if buffer_tam == 9:
                data = buffer[3:7]
                crc16_recebido = buffer[7:9]
                crc16_calculado = calcula_CRC(buffer[0:7], 7).to_bytes(2, 'little')

                if crc16_recebido == crc16_calculado:
                   # print('Mensagem recebida 2: {}'.format(buffer))
                    return data
                else:
                   # print('Mensagem recebida 3: {}'.format(buffer))
                    print('CRC16 invalido')
                    self.recebe()
            else:
               # print('Mensagem recebida 4: {}'.format(buffer))
               # print('Mensagem no formato incorreto, tamanho: {}'.format(buffer_tam))
                self.recebe()
        else:
            self.conecta()
            return None
