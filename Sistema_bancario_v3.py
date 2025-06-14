"""
Sistema Bancário - v 3.0
Desenvolvido por: [Victória Meira]
Modelagem com Programação Orientada a Objetos (POO).
"""

from abc import ABC, abstractmethod
from datetime import datetime

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @property
    @abstractmethod
    def data(self):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        self._data = datetime.now()

    @property
    def valor(self):
        return -self._valor

    @property
    def data(self):
        return self._data

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        self._data = datetime.now()

    @property
    def valor(self):
        return self._valor

    @property
    def data(self):
        return self._data

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao: Transacao):
        self.transacoes.append(transacao)

    def gerar_extrato(self):
        linhas = []
        for t in self.transacoes:
            tipo = "Depósito" if t.valor > 0 else "Saque"
            linhas.append(f"{t.data.strftime('%Y-%m-%d %H:%M:%S')} - {tipo}: R$ {abs(t.valor):.2f}")
        return "\n".join(linhas)

class Cliente:
    def __init__(self, nome, cpf, endereco):
        self.nome = nome
        self.cpf = cpf
        self.endereco = endereco

    def __str__(self):
        return f"{self.nome} - CPF: {self.cpf}"

class Conta:
    def __init__(self, agencia, numero, cliente: Cliente):
        self.agencia = agencia
        self.numero = numero
        self.cliente = cliente
        self.saldo = 0.0
        self.historico = Historico()

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.historico.adicionar_transacao(Deposito(valor))
            print("Depósito realizado com sucesso.")
        else:
            print("Valor inválido para depósito.")

    def sacar(self, valor):
        if valor <= 0:
            print("Valor inválido para saque.")
            return False

        if valor > self.saldo:
            print("Saldo insuficiente.")
            return False

        self.saldo -= valor
        self.historico.adicionar_transacao(Saque(valor))
        print("Saque realizado com sucesso.")
        return True

    def extrato(self):
        print("\n===== EXTRATO =====")
        print(self.historico.gerar_extrato() or "Nenhuma transação realizada.")
        print(f"Saldo atual: R$ {self.saldo:.2f}")
        print("=" * 20)

    def __str__(self):
        return f"Agência: {self.agencia} | Conta: {self.numero} | Titular: {self.cliente.nome}"

class ContaCorrente(Conta):
    def __init__(self, agencia, numero, cliente, limite=500.0, limite_saques=3):
        super().__init__(agencia, numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_realizados = 0

    def sacar(self, valor):
        if self.saques_realizados >= self.limite_saques:
            print("Limite de saques diários atingido.")
            return False

        if valor > self.saldo + self.limite:
            print("Saldo + limite insuficiente.")
            return False

        sucesso = super().sacar(valor if valor <= self.saldo else self.saldo)
        if sucesso:
            self.saques_realizados += 1
        return sucesso

class Banco:
    AGENCIA_PADRAO = "0001"

    def __init__(self):
        self.clientes = []
        self.contas = []

    def criar_cliente(self, nome, cpf, endereco):
        if self.buscar_cliente(cpf):
            print("Cliente já cadastrado!")
            return None
        cliente = Cliente(nome, cpf, endereco)
        self.clientes.append(cliente)
        print("Cliente criado com sucesso!")
        return cliente

    def buscar_cliente(self, cpf):
        for c in self.clientes:
            if c.cpf == cpf:
                return c
        return None

    def criar_conta_corrente(self, cpf):
        cliente = self.buscar_cliente(cpf)
        if not cliente:
            print("Cliente não encontrado!")
            return None
        numero = len(self.contas) + 1
        conta = ContaCorrente(self.AGENCIA_PADRAO, numero, cliente)
        self.contas.append(conta)
        print("Conta corrente criada com sucesso!")
        return conta

    def autenticar_conta(self, cliente, conta):
        return conta in self.contas and conta.cliente is cliente

    def listar_contas(self):
        print("\n=== CONTAS ===")
        for conta in self.contas:
            print(conta)
        print("==============")

def menu():
    return input("""
[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo cliente
[nc] Nova conta
[lc] Listar contas
[q] Sair
=> """)

def main():
    banco = Banco()
    while True:
        opc = menu()

        if opc == "d":
            cpf = input("CPF do cliente: ")
            conta = next((c for c in banco.contas if c.cliente.cpf == cpf), None)
            if conta:
                valor = float(input("Valor do depósito: "))
                conta.depositar(valor)
            else:
                print("Cliente/conta não encontrado!")

        elif opc == "s":
            cpf = input("CPF do cliente: ")
            conta = next((c for c in banco.contas if c.cliente.cpf == cpf), None)
            if conta:
                valor = float(input("Valor do saque: "))
                conta.sacar(valor)
            else:
                print("Cliente/conta não encontrado!")

        elif opc == "e":
            cpf = input("CPF do cliente: ")
            conta = next((c for c in banco.contas if c.cliente.cpf == cpf), None)
            if conta:
                conta.extrato()
            else:
                print("Cliente/conta não encontrado!")

        elif opc == "nu":
            nome = input("Nome completo: ")
            cpf = input("CPF (apenas números): ")
            endereco = input("Endereço: ")
            banco.criar_cliente(nome, cpf, endereco)

        elif opc == "nc":
            cpf = input("CPF do cliente para criar conta: ")
            banco.criar_conta_corrente(cpf)

        elif opc == "lc":
            banco.listar_contas()

        elif opc == "q":
            break

        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()
