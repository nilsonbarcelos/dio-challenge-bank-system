from datetime import date

menu =  '''

====================================================

|B|D| Banco Digital - Selecione uma das operações:

[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair

>>> '''

balance = 0
daily_limit = float(500)
bank_statment = []
allowed_withdraw = 0
WITHDRAW_LIMIT = 3

def register_operation (current_date, operation, value):
    bank_statment_operation = {
        "date": str(current_date),
        "operation": str(operation),
        "value": str(value)
    } 
    bank_statment.append(bank_statment_operation)


def get_bank_statment(current_date):
    print("====================================================")
    print(f"|B|D - Extrato - Dia: {current_date}")
    print("----------------------------------------------------")
    print(f"Saldo: {balance}")
    print("-------------------- Detalhe -----------------------")
    for bst in bank_statment:
        bst_date = bst['date']
        bst_operation = bst['operation']
        bst_value = bst['value']
        print("----------------------------------------------------")
        print(f"Data: {bst_date}  |  {bst_operation}  | R$ {bst_value}")
        print("----------------------------------------------------")
    print("====================================================")

while (True):

    operation = input(menu)
    current_date = date.today()
    
    if operation == '1':
        try:
            deposit_value = float(input('Digite o valor a ser depositado >>> R$ '))
            if deposit_value > 0:
                balance += deposit_value
                register_operation(current_date,"Depósito", deposit_value)
                print(f"Deposito no valor de R$ {deposit_value} realizado com sucesso!")
            else:
                print("Valor inválido")
        except:
            print('Valor inválido')
        
    elif operation == '2':
        try:
            withdraw_value = float(input('Digite o valor a sacar >>> R$ '))
            if withdraw_value < 0:
                print("Valor inválido")
            elif allowed_withdraw >= WITHDRAW_LIMIT:
                print("Limite de saque excedido")
            elif withdraw_value > daily_limit:
                print("Valor excede o valor máximo permitido")
            elif withdraw_value > balance:
                print("Saldo insuficiente")
            else:
                allowed_withdraw += 1
                balance -= withdraw_value
                register_operation(current_date, "Saque", withdraw_value)
                print(f'Saque no valor {withdraw_value} realizado com sucesso')
        except:
            print('Valor inválido')

    elif operation == '3':
        get_bank_statment(current_date)
        
    elif operation == '4':
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada")