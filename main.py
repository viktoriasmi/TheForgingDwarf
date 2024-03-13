# import psycopg2
import sqlite3
import hashlib
import getpass
# def connect_database():
#     try:
#         # con = psycopg2.connect(database="postgres", user="postgres", password="1111", port="5432", host="localhost")
#         con = psycopg2.connect(database="theforgingdwarf", user="postgres", password="1111", port="5432", host="localhost")
#         # cur = con.cursor()
#         # con.autocommit = True
#         # cur.execute("CREATE DATABASE TheForgingDwarf;")
#
#         # print("Информация о сервере PostgreSQL")
#         # print(con.get_dsn_parameters(), "\n")
#         # cur.execute("SELECT version();")
#         # record = cur.fetchone()
#         # print("Вы подключены к - ", record, "\n")
#         return con
#     except:
#         print('Не удалось подключиться к базе данных')
#         return None

def connect_database():
    db = sqlite3.connect('TheForgingDwarf.db')
    return db

def create_tables():
    con = connect_database()
    if con is not None:
        cur = con.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        address TEXT NOL NULL
        );
        """)
        con.commit()

        cur.execute("""
                CREATE TABLE IF NOT EXISTS catalog (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                material TEXT NOT NULL,
                style TEXT NOT NULL,
                description TEXT,
                production_time INT NOT NULL,
                price DECIMAL(10, 2)
                );
                """)
        con.commit()

        cur.execute("""
                        CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_id INT REFERENCES clients(id),
                        catalog_id INT REFERENCES catalog(id),
                        created_at TIMESTAMP,
                        completed_at TIMESTAMP,
                        amount INT NOT NULL,
                        status TEXT NOT NULL
                        );  
                        """)
        con.commit()

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS individual_orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id INT REFERENCES clients(id),
                    req TEXT,
                    created_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    amount INT NOT NULL,
                    status TEXT NOT NULL
                    );
                    """)

        cur.execute("""
                CREATE TABLE IF NOT EXISTS income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INT REFERENCES orders(id),
                amount NUMERIC,
                created_at TIMESTAMP
                );
                """)
        con.commit()

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS queue (
                    order_id INT REFERENCES orders(id),
                    created_at TIMESTAMP REFERENCES orders(created_at),
                    status TEXT NOT NULL REFERENCES orders(status),
                    production_time INT NOT NULL REFERENCES catalog(production_time)
                    );
                    """)
        con.commit()
        cur.execute("""
                            CREATE TABLE IF NOT EXISTS users (
                            username text,
                            password text
                            );
                            """)
        con.commit()
        con.close()

clients1 = [('Ричард', 'Торрес', '9902 Майерт Ленд Соледадвилль'),('Дебра', 'Флорес', '5390 Люкс Вивьен Маунт'),('Карен', 'Бейкер', '77402 Люкс Энджел Клифф')]
catalog1 = [('Меч Экскалибур', 'холодное оружие', 'Дамасская сталь', 'Готика',  120, 10000.00), ('Скульптура Давида', 'скульптуры', 'Тигельная сталь', 'Историческое', 100, 100000.00),
            ('Средневековая броня', 'средневековая броня', 'Железо', 'Готика', 100, 10000.00),('Средневековая броня', 'средневековая броня', 'Железо', 'Готика', 100, 10000.00),
            ('Броня эпохи Возрождения','броня эпохи Возрождения', 'Дамасская сталь', 'Фэнтези', 100, 10000.00),('Меч Гарольда', 'холодное оружие', 'Дамасская сталь', 'Готика', 120, 10000.00),
            ('Ворота Тадж-Махала', 'ворота', 'Мозаичный', 'Исторический', 1000, 1000000.00),('Ворота Колизея', 'ворота', 'Мозаичная','Историческое', 900, 10000.00)]
orders1 = [(1, 2, 1, 'ip'), (2, 1, 2, 'ip'), (3, 4, 1, 'ip')]
users1 = [('user', 'useruser'), ('admin', 'adminadmin')]
def add_data():
    con = connect_database()
    if con is not None:
        cur = con.cursor()
        cur.executemany("""
                        INSERT OR IGNORE INTO clients (first_name, last_name, address) VALUES (?, ?, ?);
                        """, clients1)
        con.commit()
        cur.executemany("""
                          INSERT OR IGNORE INTO catalog (name, type, material, style, production_time, price) VALUES (?, ?, ?, ?, ?, ?);
                        """, catalog1)
        con.commit()
        cur.executemany("""
                            INSERT OR IGNORE INTO orders (client_id, catalog_id, amount, status) VALUES (?, ?, ?, ?);
                            """, orders1)
        con.commit()
        cur.execute("""
                    INSERT OR IGNORE INTO individual_orders (client_id, amount, status) VALUES (3, 1, 'ip');
                    """)
        con.commit()
        cur.execute("""
                    INSERT OR IGNORE INTO users (username, password) VALUES ('user', 'useruser');
                            """)
        con.commit()
        cur.execute("""
                    INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'adminadmin');
                                    """)
        con.commit()

def hashing_passwords():
    con = connect_database()
    cur = con.cursor()
    userpas = 'useruser'
    adminpas = 'adminadmin'
    hashed_password = hashlib.sha256(userpas.encode()).hexdigest()
    cur.execute("UPDATE users SET password=? WHERE username=?", (hashed_password, 'user'))
    hashed_password = hashlib.sha256(adminpas.encode()).hexdigest()
    cur.execute("UPDATE users SET password=? WHERE username=?", (hashed_password, 'admin'))
    con.commit()

def theforgingdwarfadmin():
    con = connect_database()
    cur = con.cursor()
    print('Добро пожаловать в кузницу The Forging Dwarf!')
    con.close()
def theforgingdwarfuser():
    con = connect_database()
    cur = con.cursor()
    print('Добро пожаловать в кузницу The Forging Dwarf!')
    con.close()

def authorization():
    con = connect_database()
    username = input("Введите имя пользователя: ")

    cur = con.cursor()
    cur.execute("SELECT  *  FROM users WHERE username=?", (username,))
    result = cur.fetchone()

    if result is not None:
        password = input("Введите пароль: ")
        #password = getpass.getpass("Введите пароль: ")

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if result[1] == hashed_password:
            if username == "user":
                print("Авторизация успешна")
                theforgingdwarfuser()
            if username == "admin":
                print("Авторизация успешна")
                theforgingdwarfadmin()
        else:
            print("Неверный пароль")
    else:
        print("Пользователь не найден")
    con.close()



create_tables()
#add_data()
hashing_passwords()
authorization()



# cur.close()
#con.close()
