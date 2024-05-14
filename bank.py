import os
menu = """
    MENU

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0.0
limite = 500.0
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        os.system('clear')
        try:
            deposito = float(input("Qual o valor que deseja depositar?\n=> R$"))
            if deposito <= 0:
                print("Valor deve ser maior que zero.")
            else:
                saldo += deposito
                extrato += f"        + {deposito:.2f}\n"

        except Exception as e:
            print(f"Um erro ocorreu: {e}")

    elif opcao == "s":
        os.system('clear')
        try:
            saque = float(input("Qual o valor que deseja sacar?\n=> R$"))
            if saque <= 0:
                print("Valor deve ser maior que zero.")
            elif numero_saques >= LIMITE_SAQUES:
                print(f"Limite de saque excedido. O limite de saques é {LIMITE_SAQUES}")
            elif saque > saldo:
                print(f"Saldo insuficiente. Seu saldo é R${saldo:.2f}")
            elif saque > limite:
                print(f"Valor do saque excedido. O limite por saque é R${limite:.2f}")
            else:
                numero_saques +=1
                saldo -= saque
                extrato += f"        - {saque:.2f}\n"
        except Exception as e:
            print(f"Um erro ocorreu: {e}")
    elif opcao == "e":
        os.system('clear')
        extrato_str = f"""

        ===========
        = Extrato =
        ===========

        RELAÇÃO DE ENTRADA E SAÍDA:

{extrato}

        SALDO: R$ {saldo:.2f}
        ===========

        """
        print(extrato_str)
    elif opcao == "q":
        break
    else:
        os.system('clear')
        print("Operacao invalida!")
