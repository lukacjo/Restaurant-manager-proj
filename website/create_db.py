import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user="root",
    passwd = "restaurantmanager"
    #,auth_plugin='mysql_native_password'
)
my_cursor = mydb.cursor()
#restaurantmanager
my_cursor.execute("CREATE DATABASE managerdatabase")
#my_cursor.execute("DROP DATABASE managerdatabase")
my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)
    
