import pymysql.cursors

conection = pymysql.connect(
    host='localhost',
    user='root',
    passwd='Mavi1234#',
    db='pythonDados',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

with conection.cursor() as cursor:
    cursor.execute('SELECT * FROM pessoas')
    data = cursor.fetchall() #traz dados do banco de dados

    for x in data:
        print(x)