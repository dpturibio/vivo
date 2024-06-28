from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PF(Cliente):
    def __init__(self, nome, dt_nasc, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.dt_nasc = dt_nasc
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente, limite=500, lim_saques=3):
        self._limite = limite
        self._lim_saques = lim_saques
        self._nro_saques = 0
        self._saldo = 0
        self._agencia = "0001"
        self._numero = numero
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico
    
    def computa_saque(self):
        self._nro_saques += 1
    
    def sacar(self, valor):
        saldo = self._saldo
        limite = self._limite
        nro_saques = self._nro_saques
        lim_saques = self._lim_saques

        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = nro_saques >= lim_saques

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        elif valor > 0:
            self._saldo -= valor
            self.computa_saque()
            print("Saque efetuado!")
            return True
        else:
            print("Operação falhou! O valor informado é inválido.")
        return False
    
    def __str__(self):
        return f"""\
            AG:\t{self.agencia}
            CC:\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito efetuado!")
        else:
            print("Operação falhou! O valor informado é inválido.")
            return False
        return True


class Historico:

    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:$M:%s")
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


def menu():
    menu = """\n
    ============== MENU PRINCIPAL ==================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova Conta
    [lc]\tListar Contas
    [nu]\tNovo usuario
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def recuperar_conta_user(usuario):
    if not usuario.contas:
        print("Usuario nao possui conta")
        return
    return usuario.contas[0]

def depositar(usuarios):
    cpf = input("Informe o cpf do usuario(apenas numeros): ")
    usuario = filtrar_user(cpf, usuarios)

    if not usuario:
        print(f"Usuario nao encontrado!")
        return
    valor = float(input("Informe o valor do deposito:"))
    transacao = Deposito(valor)
    conta = recuperar_conta_user(usuario)
    if not conta:
        return
    usuario.realizar_transacao(conta, transacao)

def sacar(usuarios):
    
    cpf = input("Informe o cpf do usuario(apenas numeros): ")
    usuario = filtrar_user(cpf, usuarios)

    if not usuario:
        print(f"Usuario nao encontrado!")
        return
    valor = float(input("Informe o valor do saque:"))
    transacao = Saque(valor)
    conta = recuperar_conta_user(usuario)
    if not conta:
        return
    usuario.realizar_transacao(conta, transacao)


def exibir_extrato(usuarios):
    cpf = input("Informe o cpf do usuario(apenas numeros): ")
    usuario = filtrar_user(cpf, usuarios)

    if not usuario:
        print(f"Usuario nao encontrado!")
        return
    conta = recuperar_conta_user(usuario)
    if not conta:
        return
    
    transacoes = conta.historico.transacoes
    extrato = ""

    print("\n================ EXTRATO ================")
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_user(usuarios):
    cpf = input("Informe o cpf do usuario(apenas numeros): ")
    usuario = filtrar_user(cpf, usuarios)
    if usuario:
        print(f"Usuario com cpf:{cpf} já existe no sistema!")
        return
    nome = input("Informe o nome completo: ")
    dt_nasc = input("Informe a data de nascimento (dd-mm-aaaa): ")
    end = input("Informe o endereço (logradouro, nro - bairro - cidade/ESTADO): ")
    usuario = PF(nome=nome, dt_nasc=dt_nasc, cpf=cpf, endereco=end)
    usuarios.append(usuario)

    print(f"Usuário {nome} cadastrado com sucesso!")


def filtrar_user(cpf, usuarios):
    filtrados = [usuario for usuario in usuarios if usuario.cpf == cpf]
    return filtrados[0] if filtrados else None


def criar_conta(nro, usuarios, contas):
    cpf = input("Informe o cpf do usuario(apenas numeros): ")
    usuario = filtrar_user(cpf, usuarios)
    
    if not usuario:
        print(f"Usuário de cpf({cpf}) não possui cadastro.")
        return    
    conta = Conta.nova_conta(cliente=usuario, numero=nro)
    contas.append(conta)
    usuario.adicionar_conta(conta)
    print(f"Conta: {nro} criada para o usuario: {usuario.nome} com sucesso!")


def listar_contas(contas):
    for cta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(cta)))


def main():

    usuarios = []
    contas = []

    while True:

        opcao = menu()

        if opcao == "d":
            depositar(usuarios)

        elif opcao == "s":
            sacar(usuarios)

        elif opcao == "e":
            exibir_extrato(usuarios)

        elif opcao == "nu":
            criar_user(usuarios)

        elif opcao == "nc":
            nro_cta = len(contas) + 1
            criar_conta(nro_cta, usuarios, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
