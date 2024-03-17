# import psycopg2
import sqlite3
import hashlib
import getpass
import datetime


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
                        production_time INT NOT NULL,
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
                    production_time INT NOT NULL,
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
                    CREATE TABLE IF NOT EXISTS queue_regular (
                    order_id INT REFERENCES orders(id),     
                    created_at TIMESTAMP,
                    status TEXT NOT NULL,
                    production_time INT NOT NULL
                    );
                    """)
        con.commit()
        cur.execute("""
                            CREATE TABLE IF NOT EXISTS queue_individual (
                            order_id INT REFERENCES individual_orders(id),     
                            created_at TIMESTAMP,
                            status TEXT NOT NULL,
                            production_time INT NOT NULL
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
orders1 = [(1, 2, '2024-03-14 15:08:05', 3, 1, 'ip'), (2, 1, '2024-03-14 15:08:05', 3, 2, 'ip'), (3, 4, '2024-03-14 15:08:05', 4, 1, 'ip')]
users1 = [('user', 'useruser'), ('admin', 'adminadmin')]
queue1 = [()]
def add_data():
    con = connect_database()
    if con is not None:
        cur = con.cursor()
        cur.executemany("""
                        INSERT INTO clients (first_name, last_name, address) VALUES (?, ?, ?);
                        """, clients1)
        con.commit()
        cur.executemany("""
                          INSERT INTO catalog (name, type, material, style, production_time, price) VALUES (?, ?, ?, ?, ?, ?);
                        """, catalog1)
        con.commit()
        cur.executemany("""
                            INSERT INTO orders (client_id, catalog_id, created_at, production_time, amount, status) VALUES (?, ?, ?, ?, ?, ?);
                            """, orders1)
        con.commit()
        cur.execute("""
                    INSERT INTO individual_orders (client_id, created_at, production_time, amount, status) VALUES (3, '2024-03-14 15:08:05', 5, 1, 'ip');
                    """)
        con.commit()
        cur.execute("""
                    INSERT INTO users (username, password) VALUES ('user', 'useruser');
                            """)
        con.commit()
        cur.execute("""
                    INSERT INTO users (username, password) VALUES ('admin', 'adminadmin');
                                    """)
        con.commit()
        cur.execute("""
            INSERT INTO queue_regular (order_id, created_at, status, production_time)
            SELECT id, created_at, status, production_time FROM orders;
        """)
        con.commit()

        cur.execute("""
            INSERT INTO queue_individual (order_id, created_at, status, production_time)
            SELECT id, created_at, status, production_time FROM individual_orders;
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
    print('Выберите одну из опций: ')
    print('1 - добавить новый заказ')
    print('2 - добавить нового клиента')
    print('3 - удалить заказ')
    print('4 - изменить заказ')
    print('5 - добавить новое изделие в каталог')
    print('6 - изменить изделие в каталоге')
    print('7 - поиск')
    print('8 - показать очередь заказов')
    print('9 - вывести доход кузницы')
    number = int(input("Выберите для продолжения: "))
    if number == 1:
        choice = input("Выберите тип заказа: индивидуальный или из каталога? (i или c) ")
        if choice == 'i':
            print('Список клиентов кузницы: ')
            cur.execute("SELECT   *   FROM clients")
            desc = cur.description
            headers = [col[0] for col in desc]
            print(headers)
            for row in cur:
                print(row)
            client_id = input("Введите id клиента: ")
            req = input("Введите описание заказа: ")
            production_time = input("Введите время производства: ")
            amount = input("Введите количество изделий: ")
            status = 'ip'
            created_at = datetime.datetime.now()
            cur.execute(
                "INSERT INTO individual_orders (client_id, req, created_at, production_time, amount, status) VALUES (?, ?, ?, ?, ?, ?)",
                (client_id, req, created_at, production_time, amount, status))
        elif choice == 'c':
            print('Список клиентов кузницы: ')
            cur.execute("SELECT  *  FROM clients")
            desc = cur.description
            headers = [col[0] for col in desc]
            print(headers)
            for row in cur:
                print(row)
            client_id = input("Введите id клиента: ")
            print('Список изделий из каталога: ')
            cur.execute("SELECT  *  FROM catalog")
            desc = cur.description
            headers = [col[0] for col in desc]
            print(headers)
            for row in cur:
                print(row)
            catalog_id = input("Введите id изделия из каталога: ")
            production_time = input("Введите время производства: ")
            amount = input("Введите количество изделий: ")
            status = 'ip'
            created_at = datetime.datetime.now()
            cur.execute(
                "INSERT INTO orders (client_id, catalog_id, created_at, production_time, amount, status) VALUES (?, ?, ?, ?, ?, ?)",
                (client_id, catalog_id, created_at, production_time, amount, status))
        con.commit()

    con.close()
def theforgingdwarfuser():
    con = connect_database()
    cur = con.cursor()
    print('Добро пожаловать в кузницу The Forging Dwarf!')
    print('Выберите одну из опций: ')
    print('1 - отправить заявку на заказ')
    print('2 - поиск')
    print('3 - вывести каталог изделий')
    number = input("Выберите для продолжения: ")
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
