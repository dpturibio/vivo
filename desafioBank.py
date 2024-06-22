import textwrap


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


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("Depósito efetuado!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, nro_saques, lim_saques):
    
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
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque efetuado!")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
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
    usuarios.append({"nome":nome, "data_nascimento":dt_nasc, "cpf":cpf, "endereco":end})

    print(f"Usuário {nome} cadastrado com sucesso!")


def filtrar_user(cpf, usuarios):
    filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return filtrados[0] if filtrados else None


def criar_conta(ag, nro, usuarios):
    cpf = input("Informe o cpf do usuario(apenas numeros): ")
    usuario = filtrar_user(cpf, usuarios)
    if usuario:
        print(f"Conta: {nro} criada para o usuario: {usuario} com sucesso!")
        return {"agencia": ag, "numero_conta": nro, "usuario": usuario}    
    print(f"Usuário de cpf({cpf}) não possui cadastro.")


def listar_contas(contas):
    for cta in contas:
        linha = f"""\
            Agencia:\t{cta['agencia']}
            C/C:\t\t{cta['numero_conta']}
            Titular:\t{cta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    usuarios = []
    contas = []

    while True:

        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                nro_saques=numero_saques,
                lim_saques=LIMITE_SAQUES
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_user(usuarios)

        elif opcao == "nc":
            nro_cta = len(contas) +1
            conta = criar_conta(AGENCIA, nro_cta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
