from datetime import date
import re


menu =  '''

====================================================

|B|D| Banco Digital - Selecione uma das operações:

[1] Depositar
[2] Sacar
[3] Extrato
[4] Cadastrar usuário
[5] Cadastrar conta corrente
[6] Listar dados do cliente
[7] Sair

>>> '''

daily_limit = float(500)
bank_statment = []
allowed_withdraw = 0
WITHDRAW_LIMIT = 3
client_list = []
bank_account_list = []
last_account_number = 0
bank_account_number_list = [0]


def _register_bank_statment (current_date,/, operation,*,value, bank_account):
    bank_statment_operation = {
        "date": str(current_date),
        "operation": str(operation),
        "value": str(value),
        "bank_account": bank_account
    } 
    bank_statment.append(bank_statment_operation)


def _get_bank_statment(current_date, bank_account):
    for bkc in bank_account_list:
        if bkc.get('account') == bank_account:
            print("====================================================")
            print(f"|B|D - Extrato - Dia: {current_date}")
            print("----------------------------------------------------")
            print(f"Saldo: {bkc.get('balance_account')} - Conta corrente: {bank_account}") 
            print("-------------------- Detalhe -----------------------")
            for bst in bank_statment:
                bst_date = bst['date']
                bst_operation = bst['operation']
                bst_value = bst['value']
                print("----------------------------------------------------")
                print(f"Data: {bst_date}  |  {bst_operation}  | R$ {bst_value}")
                print("----------------------------------------------------")
            print("====================================================")


def _deposit_value(deposit_value, current_date, bank_account, /):
    if deposit_value > 0:
        for bkc in bank_account_list:
            if bkc.get('account') == bank_account:
                current_balance_value = bkc.get('balance_account')
                current_balance_value += deposit_value
                bkc['balance_account'] = current_balance_value
                _register_bank_statment(current_date,"Depósito", value=deposit_value, bank_account=bank_account)
                print(f"Deposito no valor de R$ {deposit_value} realizado com sucesso!")
            else:
                print('Conta bancária não localizada')
    else:
        print("Valor inválido")


def _withdraw_value(*, withdraw_value, current_date, allowed_withdraw, bank_account, cpf):
    for bkc in bank_account_list:
        if bkc.get('account') == bank_account and bkc.get('cpf') == cpf:            
            if withdraw_value < 0:
                print("Valor inválido")
            elif allowed_withdraw >= WITHDRAW_LIMIT:
                print("Limite de saque excedido")
            elif withdraw_value > daily_limit:
                print("Valor excede o valor máximo permitido")
            elif withdraw_value > bkc.get('balance_account'):
                print("Saldo insuficiente")
            else:
                allowed_withdraw += 1
                current_balance_value = bkc.get('balance_account')
                current_balance_value -= withdraw_value
                bkc['balance_account'] = current_balance_value
                _register_bank_statment(current_date, "Saque", value=withdraw_value, bank_account=bank_account)
                print(f'Saque no valor {withdraw_value} realizado com sucesso')
        else:
            print("O número da conta não está cadastrada")


def _add_bank_account(last_account_number):
    print("Informe o CPF para criar uma nova conta")
    client_cpf = str(input('CPF: '))
    cpf = re.sub("[^0-9]", "", client_cpf)
    if not any(c['cpf'] == cpf for c in client_list):
        print("Cadastro de pessoa requerido para essa operação")
        return
    new_account_number = bank_account_number_list[-1] + 1
    bank_account_number_list.append(new_account_number)
    bank_account = {
        "agency": "254",
        "account" : str(new_account_number).zfill(4),
        "cpf": client_cpf,
        "balance_account": 0
    }
    bank_account_list.append(bank_account)
    for client in client_list:
        if client.get('cpf') == client_cpf:
            client['bank_account'] = [c.get('account') for c in bank_account_list if c.get('cpf') == client_cpf]
            
    print(f'Conta {str(new_account_number).zfill(4)} criada com sucesso para o CPF {client_cpf}')


def _add_client():
    print("Informe os seguintes dados")
    client_cpf = str(input('CPF: '))
    cpf = re.sub("[^0-9]", "", client_cpf)
    if not any(c['cpf'] == cpf for c in client_list):
        client_name = str(input('Nome: '))
        client_birthday = str(input('Data de nascimento: '))
        client_address_street = str(input('Logradouro: '))
        client_address_number = str(input('Número: '))
        client_address_neighborhood = str(input('Bairro: '))
        client_address_city = str(input('Cidade: '))
        client_address_state = str(input('Estado: '))
        address = f"{client_address_street} {client_address_number} {client_address_neighborhood} {client_address_city} {client_address_state}"
        client = {
            "cpf" : cpf,
            "name" : client_name,
            "birthday": client_birthday,
            "address" : address,
            "bank_account" : []
        }
        client_list.append(client)
        print('Cliente cadastrado com sucesso')
    else:
        print('Cliente já cadastrado')    


def _get_client_info(client_cpf):
    for client in client_list:
        if client.get('cpf') == client_cpf:
            print(client)

while (True):

    operation = input(menu)
    current_date = date.today()
    
    if operation == '1' or operation == '2':
        try:
            print("Informe o CPF realizar essa operação")
            client_cpf = str(input('CPF: '))
            cpf = re.sub("[^0-9]", "", client_cpf)
            if any(c['cpf'] == cpf for c in client_list):
                bank_account = str(input('Digite o número da conta >>>  '))
                if any(b['account'] == bank_account for b in bank_account_list):
                    if operation == '1':
                        deposit_value = float(input('Digite o valor a ser depositado >>> R$ '))
                        _deposit_value(deposit_value, current_date, bank_account)
                    elif operation == '2':
                        withdraw_value = float(input('Digite o valor a sacar >>> R$ '))
                        _withdraw_value(withdraw_value=withdraw_value, current_date=current_date, 
                                    allowed_withdraw=allowed_withdraw, bank_account=bank_account, cpf=cpf)
                else:
                    print('Conta não localizada')
            else:
                print('Usuário não encontrado para operação')
        except:
            print('Valor inválido')
        
    elif operation == '3':
        print("Informe o número da conta pra realizar essa operação")
        bank_account = str(input('Conta bancária: '))
        _get_bank_statment(current_date, bank_account)
    
    elif operation == '4':
        _add_client()
    
    elif operation == '5':
        _add_bank_account(last_account_number)

    elif operation == '6':
        print("Informe o CPF realizar essa operação")
        client_cpf = str(input('CPF: '))
        cpf = re.sub("[^0-9]", "", client_cpf)
        if any(c['cpf'] == cpf for c in client_list):
            _get_client_info(client_cpf=cpf)
        else:
            print('Cliente não encontrado')
    elif operation == '7':
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada")