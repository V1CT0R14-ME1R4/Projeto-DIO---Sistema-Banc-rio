"""
Sistema Bancário - v 1.0
Desenvolvido por: [Victória Meira]
Operações: Depósito, Saque, Extrato
"""

def menu():
    print("""
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Sair
    """)
    return input("Escolha uma opção: ")

def depositar(saldo, extrato):
    valor = float(input("Informe o valor do depósito: "))
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: R$ {valor:.2f}")
        print("Depósito realizado com sucesso.")
    else:
        print("Valor inválido.")
    return saldo, extrato

def sacar(saldo, extrato, limite, saques_realizados, limite_saques):
    valor = float(input("Informe o valor do saque: "))
    if valor > saldo:
        print("Saldo insuficiente.")
    elif valor > limite:
        print(f"O valor do saque excede o limite de R$ {limite:.2f}")
    elif saques_realizados >= limite_saques:
        print("Número máximo de saques atingido.")
    elif valor <= 0:
        print("Valor inválido.")
    else:
        saldo -= valor
        extrato.append(f"Saque: -R$ {valor:.2f}")
        saques_realizados += 1
        print("Saque realizado com sucesso.")
    return saldo, extrato, saques_realizados

def mostrar_extrato(saldo, extrato):
    print("\n====== EXTRATO ======")
    if not extrato:
        print("Não há movimentações.")
    else:
        for op in extrato:
            print(op)
    print(f"Saldo atual: R$ {saldo:.2f}")
    print("=====================\n")

def main():
    saldo = 0
    limite = 500
    extrato = []
    saques_realizados = 0
    LIMITE_SAQUES = 3

    while True:
        opcao = menu()

        if opcao == "1":
            saldo, extrato = depositar(saldo, extrato)

        elif opcao == "2":
            saldo, extrato, saques_realizados = sacar(
                saldo, extrato, limite, saques_realizados, LIMITE_SAQUES
            )

        elif opcao == "3":
            mostrar_extrato(saldo, extrato)

        elif opcao == "4":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()

