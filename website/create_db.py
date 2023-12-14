import mysql.connector
# tworzenia bazy danych
# tak samo connector jak w views
mydb = mysql.connector.connect(
    host = "localhost",
    user="root",
    passwd = "restaurantmanager"
    #,auth_plugin='mysql_native_password'
)

my_cursor = mydb.cursor()
#restaurantmanager
#my_cursor.execute("CREATE DATABASE managerdatabase")
#my_cursor.execute("DROP DATABASE managerdatabase") # jeeli jest problem to po prostu to odznaczam i niszcze stara baze a potem odznaczam create i tworze
my_cursor.execute("SHOW DATABASES") # to jest tylko eby pokazać jakie sa bazyu danych i zobaczyć czy sie stworzyła 
for db in my_cursor:
    print(db)
    
