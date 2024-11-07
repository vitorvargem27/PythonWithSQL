import pymysql.cursors

conection = pymysql.connect(
    host='localhost',
    user='root',
    passwd='Mavi1234#',
    db='pythonDados',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

qntdRegistros = 0

while True:
    nomePessoa = input('Qual seu nome? ')
    sobrenomePessoa = input('Qual seu sobrenome? ')
    idadePessoa = input('Qual sua idade? ')

    insertDataBase = f"insert into pessoas values('{nomePessoa}','{sobrenomePessoa}','{idadePessoa}')"


    with conection.cursor() as cursor:
        cursor.execute(insertDataBase)
        conection.commit()
        qntdRegistros += 1

    continueInclude = input('Deseja continuar? [S/N] ')
    if continueInclude.upper() == 'N':
        break

print(qntdRegistros, "registro(s) inserido(s).")