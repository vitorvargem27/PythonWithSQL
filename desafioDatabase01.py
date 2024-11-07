import pymysql.cursors

conection = pymysql.connect(
    host='localhost',
    user='root',
    passwd='Mavi1234#',
    db='pythonDados',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

while True:
    login = False
    #username = input("Qual seu nome?")
    #age = input("Qual sua idade?")
    with conection.cursor() as cursor:
        cursor.execute('SELECT * FROM pessoas')
        allData = cursor.fetchall()
        print(allData)

    for data in allData:
        nomeData = data['nome']
        if nomeData.upper() == username.upper() : #and data["idade"] == age:
            print(f"Usuário {username} de idade {age} foi logado no sistema")
            login = True
            break
    if login :
        break
    else:
        print("Nome ou idade incorretos, valide novamente.")