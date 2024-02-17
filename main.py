import psycopg2

# con = psycopg2.connect(database="postgres", user="postgres", password="1111", port="5432", host="localhost")
con = psycopg2.connect(database="theforgingdwarf", user="postgres", password="1111", port="5432", host="localhost")
cur = con.cursor()
#con.autocommit = True
#cur.execute("CREATE DATABASE TheForgingDwarf;")


# print("Информация о сервере PostgreSQL")
# print(con.get_dsn_parameters(), "\n")
# cur.execute("SELECT version();")
# record = cur.fetchone()
# print("Вы подключены к - ", record, "\n")




cur.close()
con.close()
