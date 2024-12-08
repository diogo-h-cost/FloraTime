class Agendamento:
    def __init__(self, ordem, horario, cliente, endereco, servico, valor, observacao):
        self._ordem = ordem
        self._horario = horario
        self._cliente = cliente
        self._endereco = endereco
        self._servico = servico
        self._valor = valor
        self._observacao = observacao

    @property
    def ordem(self):
        return self._ordem

    @property
    def horario(self):
        return self._horario

    @property
    def cliente(self):
        return self._cliente

    @property
    def endereco(self):
        return self._endereco

    @property
    def servico(self):
        return self._servico

    @property
    def valor(self):
        return self._valor

    @property
    def observacao(self):
        return self._observacao

    @horario.setter
    def horario(self, horario):
        self._horario = horario

    @cliente.setter
    def cliente(self, cliente):
        self._cliente = cliente

    @endereco.setter
    def endereco(self, endereco):
        self._endereco = endereco

    @servico.setter
    def servico(self, servico):
        self._servico = servico

    @valor.setter
    def valor(self, valor):
        if valor < 0:
            raise ValueError("O valor não pode ser negativo.")
        self._valor = valor

    @observacao.setter
    def observacao(self, observacao):
        self._observacao = observacao