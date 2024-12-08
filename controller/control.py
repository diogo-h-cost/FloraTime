from models.agend import Agendamento
from models.banco import Modelo

class AgendControl:
    def __init__(self):
        self.model = Modelo()
        self.agend = None

    def valida_login(self, user, password):
        login = self.model.valida_login()
        if user == login[1] and password == login[2]:
            return True
        else:
            return False

    def create(self, horario, cliente, endereco, servico, valor, observacao):
        agd = Agendamento(None, horario, cliente, endereco, servico, float(valor), observacao)
        return self.model.insert(agd)

    def read(self, ordem):
        self.agend = self.model.select(int(ordem))
        if self.agend != None:
            return self.agend
        self.agend = None
        return None

    def read_all(self):
        agendamentos = self.model.select_all()
        return agendamentos

    def update(self, ordem, horario, cliente, endereco, servico, valor, observacao):
        self.agend = self.model.select(int(ordem))
        if self.agend != None:
            self.agend.horario = horario
            self.agend.cliente = cliente
            self.agend.endereco = endereco
            self.agend.servico = servico
            self.agend.valor = float(valor)
            self.agend.observacao = observacao
            return self.model.update(self.agend)
        self.agend = None
        return None

    def delete(self, ordem):
        return self.model.delete(ordem)