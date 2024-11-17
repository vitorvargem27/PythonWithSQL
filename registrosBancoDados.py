import pymysql.cursors

conection = pymysql.connect(
    host='localhost',
    user='root',
    passwd='Mavi1234#',
    db='pizzaria',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

def OrderStatistic() :
    nomeProdutos = []
    nomeProdutos.clear()

    with conection.cursor() as cursor:
        cursor.execute('SELECT * FROM pedidos')
        produtosData = cursor.fetchall()
        

def createOrder() :
    continuarPedido = True
    with conection.cursor() as cursor:
        cursor.execute("SELECT nome_cliente, username_cliente FROM clientes")
        dadoCliente = cursor.fetchall()
        for cliente in dadoCliente :
            nomeCliente = cliente['nome_cliente']
            while continuarPedido :
                user = str(input("Digite o username do cliente que fará o pedido :\n"))
                if user in cliente['username_cliente']:
                    pedidoCliente = str(input("Digite seu pedido : \n - PIZZA \n - LANCHE\n")).upper()
                    if pedidoCliente == 'PIZZA' :
                        cursor.execute(f"INSERT INTO pedidos (nome_cliente,pedido_cliente, ingredientes_pedido)"
                                       f" VALUES ('{nomeCliente}'"
                                       f",'{pedidoCliente}',"
                                       f"'mussarela, tomate')")
                        conection.commit()
                        print(f"Pedido {pedidoCliente} adicionado com sucesso!")
                        continuarPedido = False

                    elif pedidoCliente == 'LANCHE' :
                        cursor.execute(f"INSERT INTO pedidos (nome_cliente,pedido_cliente, ingredientes_pedido)"
                                       f" VALUES ('{nomeCliente}'"
                                       f",'{pedidoCliente}',"
                                       f"'pão, queijo')")
                        conection.commit()
                        print(f"Pedido {pedidoCliente} adicionado com sucesso!")
                        continuarPedido = False

                else :
                    print("Usuário inexistente")

def readData() :
    with conection.cursor() as cursor :
        cpfUsuario = input(str("Digite o CPF do seu usuário abaixo para ver seus dados :\n"))
        cursor.execute(f'SELECT * FROM clientes WHERE cpf_cliente = {cpfUsuario}')
        data = cursor.fetchall()
        for dataUser in data :
            print(f"Nome do cliente : {dataUser['nome_cliente']}")
            print(f"CPF do cliente : {dataUser['cpf_cliente']}")
            print(f"Usuário do cliente : {dataUser['username_cliente']}")
            print(f"Id do cliente : {dataUser['id_cliente']}")

def updateData() :
    with conection.cursor() as cursor :
        cpfUsuario = input("Indique o CPF do usuário que será alterado :\n")
        cursor.execute(f'SELECT * FROM clientes WHERE cpf_cliente = {cpfUsuario}')
        data = cursor.fetchall()
        for dataUser in data :
            print(f"Nome do Usuário atual : {dataUser['nome_cliente']}")
            print(f"CPF do cliente : {dataUser['cpf_cliente']}")
            print(f"Username do usuário atual : {dataUser['username_cliente']}")
            escolhaMudanca = int(input("Escolha o que deseja alterar :\n"
                                       "[1] Nome do usuário\n"
                                       "[2] Username do Usuário\n"
                                       "[3] Ambos\n"))
            if escolhaMudanca == 1 :
                nomeModificado = str(input("Digite o novo nome do usuário abaixo :\n"))
                cursor.execute(f"UPDATE clientes SET nome_cliente = '{nomeModificado}'"
                               f" WHERE cpf_cliente = '{cpfUsuario}'")
                conection.commit()
            elif escolhaMudanca == 2 :
                usernameModificado = str(input("Escreva abaixo o novo username para o usuário\n"))
                cursor.execute(f"UPDATE clientes SET username_cliente = '{usernameModificado}'"
                               f" WHERE cpf_cliente = '{cpfUsuario}'")
                conection.commit()
            elif escolhaMudanca == 3 :
                nomeModificado = str(input("Digite o novo nome do usuário abaixo :\n"))
                usernameModificado = str(input("Escreva abaixo o novo username para o usuário\n"))
                cursor.execute(f"UPDATE clientes SET nome_cliente = '{nomeModificado}',"
                               f"username_cliente = '{usernameModificado}'"
                               f" WHERE cpf_cliente = '{cpfUsuario}'")
                conection.commit()



def delete() :
    continuarExclusao = True
    while continuarExclusao :
        with conection.cursor() as cursor :
            print("Para excluir seu usuário, basta digitar seu CPF abaixo:")
            cpfClienteExclusao = input('Digite o seu cpf:\n ')
            cursor.execute(f'DELETE FROM clientes WHERE cpf_cliente = {cpfClienteExclusao}')
            conection.commit()
            print(f"Cliente com o CPF {cpfClienteExclusao} excluído com sucesso")
            seguirExclusao = input("Deseja excluir outro usuário?[S/N]").upper()
            if seguirExclusao == 'N':
                continuarExclusao = False
                break

def create() :
    with conection.cursor() as cursor :
        nomeCliente = str(input('Digite o seu nome:\n '))
        cpfCliente = str(input('Digite o seu cpf:\n '))
        usernameCliente = str(input('Crie o seu username:\n '))
        passwordCliente = str(input('Crie o seu password:\n '))
        cursor.execute(f"insert into clientes(nome_cliente,"
                       "cpf_cliente,"
                       "username_cliente,"
                       "password_cliente) "
                       f"values('{nomeCliente}'"
                       f",'{cpfCliente}'"
                       f",'{usernameCliente}'"
                       f",'{passwordCliente}')")
        conection.commit()
        print('Usuário criado com sucesso!')

def choice_Options() :
    print("Opções dentro da plataforma:\n"
          "[1] Adicionar\n"
          "[2] Excluir\n"
          "[3] Editar\n"
          "[4] Ver dados\n"
          "[5] Realizar pedido\n")
    choice_Value = int(input('O que você deseja fazer?\n'))
    return choice_Value

def authenticated():
    loginUser = False
    with conection.cursor() as cursor:
        cursor.execute('SELECT * FROM clientes')
        allUsers = cursor.fetchall()

        while loginUser == False:
            perguntaUser = input("Digite seu usuário :\n")
            perguntaPassword = input("Digite seu senha :\n")
            for user in allUsers:
                if user['username_cliente'] == perguntaUser and user['password_cliente'] == perguntaPassword:
                    loginUser = True
                    print(f'{user['nome_cliente']} Logado com Sucesso')
                    break
                else:
                    print(f'Verifique os dados novamente!')
    return loginUser

if authenticated() :
    choice = choice_Options()
    if choice == 1 :
        create()
    elif choice == 2 :
        delete()
    elif choice == 3 :
        updateData()
    elif choice == 4 :
        readData()
    elif choice == 5 :
        createOrder()