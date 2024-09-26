# Variáveis globais para usuários e contas
usuarios = []
contas = []
numero_conta_sequencial = 1
AGENCIA = "0001"

# Função para cadastrar um usuário
def cadastrar_usuario(nome, data_nascimento, cpf, endereco):
    # Verifica se já existe um usuário com o mesmo CPF
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            print("Já existe um usuário com esse CPF.")
            return
    
    # Cadastro do novo usuário
    novo_usuario = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    }
    usuarios.append(novo_usuario)
    print(f"Usuário {nome} cadastrado com sucesso!")

# Função para cadastrar uma conta bancária vinculada a um usuário
def cadastrar_conta(usuario):
    global numero_conta_sequencial
    nova_conta = {
        "agencia": AGENCIA,
        "numero_conta": numero_conta_sequencial,
        "usuario": usuario,
        "saldo": 0,
        "limite": 500,
        "numero_saques": 0,
        "extrato": ""
    }
    contas.append(nova_conta)
    numero_conta_sequencial += 1
    print(f"Conta {nova_conta['numero_conta']} cadastrada para {usuario['nome']}!")

# Função de depósito
def deposito(conta, valor):
    if valor > 0:
        conta["saldo"] += valor
        conta["extrato"] += f"Depósito: R$ {valor:.2f}\n"
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return conta["saldo"], conta["extrato"]

# Função de saque, recebe argumentos por nome
def saque(*, conta, valor):
    excedeu_saldo = valor > conta["saldo"]
    excedeu_limite = valor > conta["limite"]
    excedeu_saques = conta["numero_saques"] >= 3

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        conta["saldo"] -= valor
        conta["extrato"] += f"Saque: R$ {valor:.2f}\n"
        conta["numero_saques"] += 1
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    
    return conta["saldo"], conta["extrato"]

# Função para exibir o extrato, recebe argumentos por posição e nome
def exibir_extrato(conta, /, *, saldo):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not conta["extrato"] else conta["extrato"])
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

# Função para listar os usuários cadastrados
def listar_usuarios():
    if not usuarios:
        print("Nenhum usuário cadastrado.")
    else:
        print("\n===== USUÁRIOS CADASTRADOS =====")
        for usuario in usuarios:
            print(f"Nome: {usuario['nome']}, CPF: {usuario['cpf']}, Endereço: {usuario['endereco']}")
        print("================================")

# Função para listar as contas cadastradas
def listar_contas():
    if not contas:
        print("Nenhuma conta cadastrada.")
    else:
        print("\n===== CONTAS CADASTRADAS =====")
        for conta in contas:
            print(f"Agência: {conta['agencia']}, Número da Conta: {conta['numero_conta']}, Titular: {conta['usuario']['nome']}")
        print("================================")

# Exemplo de menu interativo
menu = """

[u] Cadastrar Usuário
[c] Cadastrar Conta
[d] Depositar
[s] Sacar
[e] Extrato
[l] Listar Usuários
[k] Listar Contas
[q] Sair

=> """

while True:
    opcao = input(menu)

    if opcao == "u":
        nome = input("Informe o nome: ")
        data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
        cpf = input("Informe o CPF (somente números): ")
        endereco = input("Informe o endereço (logradouro, n° - bairro - cidade/uf): ")
        cadastrar_usuario(nome, data_nascimento, cpf, endereco)

    elif opcao == "c":
        cpf = input("Informe o CPF do usuário: ")
        usuario = next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)
        if usuario:
            cadastrar_conta(usuario)
        else:
            print("Usuário não encontrado.")

    elif opcao == "d":
        numero_conta = int(input("Informe o número da conta: "))
        conta = next((conta for conta in contas if conta["numero_conta"] == numero_conta), None)
        if conta:
            valor = float(input("Informe o valor do depósito: "))
            conta["saldo"], conta["extrato"] = deposito(conta, valor)
        else:
            print("Conta não encontrada.")

    elif opcao == "s":
        numero_conta = int(input("Informe o número da conta: "))
        conta = next((conta for conta in contas if conta["numero_conta"] == numero_conta), None)
        if conta:
            valor = float(input("Informe o valor do saque: "))
            conta["saldo"], conta["extrato"] = saque(conta=conta, valor=valor)
        else:
            print("Conta não encontrada.")

    elif opcao == "e":
        numero_conta = int(input("Informe o número da conta: "))
        conta = next((conta for conta in contas if conta["numero_conta"] == numero_conta), None)
        if conta:
            exibir_extrato(conta, saldo=conta["saldo"])
        else:
            print("Conta não encontrada.")

    elif opcao == "l":
        listar_usuarios()

    elif opcao == "k":
        listar_contas()

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
