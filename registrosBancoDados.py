import pymysql.cursors

conection = pymysql.connect(
    host='localhost',
    user='root',
    passwd='Mavi1234#',
    db='pizzaria',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

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

def delete() :
    with conection.cursor() as cursor :
        cursor.execute('SELECT username_cliente, password_cliente FROM clientes')


def choice_Options() :
    print("Opções dentro da plataforma:\n"
          "[1] Adicionar\n"
          "[2] Editar\n"
          "[3] Excluir\n"
          "[4] Ver dados")
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
