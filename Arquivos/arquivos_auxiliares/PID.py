# PID - monitora a temperatura interna e utiliza a temperatura de referência como base pra
# saber como proceder no forno.

class PID:
    kp = 30.0  # Var. do Controle Proporcional
    ki = 0.2  # Var. do Controle Integral
    kd = 400.0  # Var. do Controle Derivativo

    tempo = 1.0
    erroTotal = 0.0
    erroAnterior = 0.0
    
    controleMax = 100.0
    controleMin = -100.0
    controleStd = 0.0

    def pidAtualizaReferencia(referencia_):
        global referencia
        referencia = referencia_

    def controlePid(self, referencia, saida_medida):
        erro = referencia - saida_medida
        self.erroTotal += erro # Parte do controle integral. Vai acumulando o erro

        if self.erroTotal >= self.controleMax:
            self.erroTotal = self.controleMax
        elif self.erroTotal <= self.controleMin:
            self.erroTotal = self.controleMin
        
        delta_error = erro - self.erroAnterior # Diferença entre os erros (Termo Derivativo)
        self.controleStd = self.kp * erro + (self.ki * self.tempo) * self.erroTotal + (self.kd / self.tempo) * delta_error # PID calcula sinal de controle

        if self.controleStd >= self.controleMax:
            self.controleStd = self.controleMax
        elif self.controleStd <= self.controleMin:
            self.controleStd = self.controleMin
        
        self.erroAnterior = erro

        return self.controleStd
