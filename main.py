import psycopg2

con = psycopg2.connect(database="TheForgingDwarf", user="postgres", password="1111", port="5432", host="localhost")
cur = con.cursor()

#print("Информация о сервере PostgreSQL")
#print(con.get_dsn_parameters(), "\n")
#cur.execute("SELECT version();")
#record = cur.fetchone()
#print("Вы подключены к - ", record, "\n")




cur.close()
con.close()
