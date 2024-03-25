# import psycopg2
import sqlite3
import hashlib
import getpass
import datetime
import random


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
        cur.execute("SELECT  *  FROM clients ")
        existing_row = cur.fetchone()
        if existing_row is None:
            cur.executemany("""
                            INSERT INTO clients (first_name, last_name, address) VALUES (?, ?, ?);
                            """, clients1)
            con.commit()
        cur.execute("SELECT  *  FROM catalog ")
        existing_row = cur.fetchone()
        if existing_row is None:
            cur.executemany("""
                              INSERT INTO catalog (name, type, material, style, production_time, price) VALUES (?, ?, ?, ?, ?, ?);
                            """, catalog1)
            con.commit()
        cur.execute("SELECT  *  FROM orders ")
        existing_row = cur.fetchone()
        if existing_row is None:
            cur.executemany("""
                                INSERT INTO orders (client_id, catalog_id, created_at, production_time, amount, status) VALUES (?, ?, ?, ?, ?, ?);
                                """, orders1)
            con.commit()
        cur.execute("SELECT  *  FROM individual_orders ")
        existing_row = cur.fetchone()
        if existing_row is None:
            cur.execute("""
                        INSERT INTO individual_orders (client_id, created_at, production_time, amount, status) VALUES (3, '2024-03-14 15:08:05', 5, 1, 'ip');
                        """)
            con.commit()
        cur.execute("SELECT  *  FROM users ")
        existing_row = cur.fetchone()
        if existing_row is None:
            cur.execute("""
                        INSERT INTO users (username, password) VALUES (?, ?);
                                """, users1)
            con.commit()
        cur.execute("SELECT  *  FROM queue_regular ")
        existing_row = cur.fetchone()
        if existing_row is None:
            cur.execute("""
                INSERT INTO queue_regular (order_id, created_at, status, production_time)
                SELECT id, created_at, status, production_time FROM orders;
            """)
            con.commit()
        cur.execute("SELECT  *  FROM queue_individual ")
        existing_row = cur.fetchone()
        if existing_row is None:
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


def add_client():
    global client_id
    con = connect_database()
    cur = con.cursor()
    lastname = input("Введите фамилию: ")
    firstname = input("Введите имя: ")
    address = input("Введите адрес: ")
    cur.execute("INSERT INTO clients (last_name, first_name, address) VALUES (?, ?, ?)",
                (lastname, firstname, address))
    con.commit()
    print('Клиент успешно добавлен! ')
    client_id = cur.lastrowid

def theforgingdwarfadmin():
    con = connect_database()
    cur = con.cursor()
    while True:
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
            #индивидуальный заказ
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
            #заказ из каталога
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
                cur.execute("SELECT production_time FROM catalog WHERE id = ?", (catalog_id,))
                production_time = cur.fetchone()[0]
                amount = input("Введите количество изделий: ")
                status = 'ip'
                created_at = datetime.datetime.now()
                cur.execute(
                    "INSERT INTO orders (client_id, catalog_id, created_at, production_time, amount, status) VALUES (?, ?, ?, ?, ?, ?)",
                    (client_id, catalog_id, created_at, production_time, amount, status))
            con.commit()
            print('Заказ успешно добавлен!')
        #добавить клиента
        elif number == 2:
            con = connect_database()
            cur = con.cursor()
            lastname = input("Введите фамилию: ")
            firstname = input("Введите имя: ")
            address = input("Введите адрес: ")
            cur.execute("INSERT INTO clients (last_name, first_name, address) VALUES (?, ?, ?)",
                        (lastname, firstname, address))
            con.commit()
            print('Клиент успешно добавлен! ')
        elif number == 3:
            # удаление заказа админ
            con = connect_database()
            cur = con.cursor()
            print('Список заказов из каталога: ')
            cur.execute("SELECT  *  FROM orders")
            desc = cur.description
            headers = [col[0] for col in desc]
            print(headers)
            for row in cur:
                print(row)
            print('Список индивидуальных заказов: ')
            cur.execute("SELECT  *  FROM individual_orders")
            desc = cur.description
            headers = [col[0] for col in desc]
            print(headers)
            for row in cur:
                print(row)

            print("Выберите, где изменить заказ:")
            print("1. Изменить заказ в таблице orders")
            print("2. Изменить заказ в таблице individual_orders")
            choice = input()
            id = input("Введите id заказа для удаления: ")

            if choice == "1":
                cur.execute("DELETE FROM orders WHERE id = ?", (id,))
            elif choice == "2":
                cur.execute("DELETE FROM individual_orders WHERE id = ?", (id,))
            else:
                print("Неверный выбор. Попробуйте еще раз.")
                return
            con.commit()

            print("Заказ успешно удален.")
        elif number == 4:
            #изменение заказа админ
            con = connect_database()
            cur = con.cursor()
            print('Список заказов из каталога: ')
            cur.execute("SELECT  *  FROM orders")
            desc = cur.description
            headers = [col[0] for col in desc]
            print(headers)
            for row in cur:
                print(row)
            print('Список индивидуальных заказов: ')
            cur.execute("SELECT  *  FROM individual_orders")
            desc = cur.description
            headers = [col[0] for col in desc]
            print(headers)
            for row in cur:
                print(row)


            print("Выберите, где изменить заказ:")
            print("1. Изменить заказ в таблице orders")
            print("2. Изменить заказ в таблице individual_orders")
            choice = input("Введите номер: ")
            if choice == "1":
                # Изменение заказа в таблице orders
                print("Введите id заказа для изменения: ")
                id = input("Введите id: ")
                try:
                    # Проверка ввода на валидность
                    int(id)
                except ValueError:
                    print("Неверный ввод. Попробуйте еще раз.")
                    # Запрос на поле для изменения

                print("Выберите поле для изменения:")
                print("1. id")
                print("2. client_id")
                print("3. catalog_id")
                print("4. created_at")
                print("5. production_time")
                print("6. amount")
                print("7. status")
                choice = input("Введите номер: ")
                if choice == "1" or choice == "2" or choice == "3" or choice == "4" or choice == "5" or choice == "6" or choice == "7":
                    # Запрос на новое значение для поля

                    print("Введите новое значение для выбранного поля: ")
                    new_value = input("Введите новое значение: ")
                    try:
                        # Проверка ввода на валидность
                        if choice == "1" or choice == "2" or choice == "3":
                            int(new_value)
                        elif choice == "4":
                            date_object = datetime.datetime.strptime(new_value, '%Y-%m-%d %H:%M:%S')
                            formatted_date = date_object.strftime('%Y-%m-%d %H:%M:%S')
                            # Проверка на формат даты
                            #try:
                                #datetime.strptime(new_value, '%Y-%m-%d %H:%M:%S')
                            #except ValueError:
                                #print("Неверный формат даты. Попробуйте еще раз.")
                        elif choice == "5":
                            int(new_value)
                        elif choice == "6":
                            int(new_value)
                        elif choice == "7":
                            new_value = new_value.lower()
                            if new_value not in ['ip', 'd', 'c']:
                                print("Неверное значение статуса. Попробуйте еще раз.")
                        else:
                            print("Неверный выбор. Попробуйте еще раз.")

                    except ValueError:
                        print("Неверный ввод. Попробуйте еще раз.")

                    # Изменение данных в базе данных
                    if choice == "1":
                        cur.execute("UPDATE orders SET id = ? WHERE id = ?", (new_value, id))
                    elif choice == "2":
                        cur.execute("UPDATE individual_orders SET client_id = ? WHERE id = ?", (new_value, id))
                    elif choice == "3":
                        cur.execute("UPDATE individual_orders SET catalog_id = ? WHERE id = ?", (new_value, id))
                    elif choice == "4":
                        cur.execute("UPDATE individual_orders SET created_at = ? WHERE id = ?", (formatted_date, id))
                    elif choice == "5":
                        cur.execute("UPDATE individual_orders SET production_time = ? WHERE id = ?", (new_value, id))
                    elif choice == "6":
                        cur.execute("UPDATE individual_orders SET amount = ? WHERE id = ?", (new_value, id))
                    elif choice == "7":
                        cur.execute("UPDATE individual_orders SET status = ? WHERE id = ?", (new_value, id))

                    # Сохранение изменений в базе данных
                    con.commit()
                    print("Заказ успешно изменен!")
                else:
                    print("Неверный выбор. Попробуйте еще раз.")

            elif choice == "2":
                # Изменение заказа в таблице individual_orders
                print("Введите id заказа для изменения: ")
                id = input("Введите id: ")
                try:
                    # Проверка ввода на валидность
                    int(id)
                except ValueError:
                    print("Неверный ввод. Попробуйте еще раз.")
                    # Запрос на поле для изменения

                print("Выберите поле для изменения:")
                print("1. id")
                print("2. client_id")
                print("3. req")
                print("4. created_at")
                print("5. production_time")
                print("6. amount")
                print("7. status")
                choice = input("Введите номер: ")
                if choice == "1" or choice == "2" or choice == "3" or choice == "4" or choice == "5" or choice == "6" or choice == "7":
                    # Запрос на новое значение для поля

                    print("Введите новое значение для выбранного поля: ")
                    new_value = input("Введите новое значение: ")
                    try:
                        # Проверка ввода на валидность
                        if choice == "1" or choice == "2":
                            int(new_value)
                        elif choice == "3":
                            str(new_value)
                        elif choice == "4":
                            pass
                            # Проверка на формат даты
                            #try:
                                #datetime.strptime(new_value, '%Y-%m-%d %H:%M:%S')
                            #except ValueError:
                                #print("Неверный формат даты. Попробуйте еще раз.")
                        elif choice == "5":
                            int(new_value)
                        elif choice == "6":
                            int(new_value)
                        elif choice == "7":
                            new_value = new_value.lower()
                            if new_value not in ['ip', 'd', 'c']:
                                print("Неверное значение статуса. Попробуйте еще раз.")
                        else:
                            print("Неверный выбор. Попробуйте еще раз.")

                    except ValueError:
                        print("Неверный ввод. Попробуйте еще раз.")

                    # Изменение данных в базе данных
                    if choice == "1":
                        cur.execute("UPDATE orders SET id = ? WHERE id = ?", (new_value, id))
                    elif choice == "2":
                        cur.execute("UPDATE individual_orders SET client_id = ? WHERE id = ?", (new_value, id))
                    elif choice == "3":
                        cur.execute("UPDATE individual_orders SET req = ? WHERE id = ?", (new_value, id))
                    elif choice == "4":
                        cur.execute("UPDATE individual_orders SET created_at = ? WHERE id = ?", (new_value, id))
                    elif choice == "5":
                        cur.execute("UPDATE individual_orders SET production_time = ? WHERE id = ?", (new_value, id))
                    elif choice == "6":
                        cur.execute("UPDATE individual_orders SET amount = ? WHERE id = ?", (new_value, id))
                    elif choice == "7":
                        cur.execute("UPDATE individual_orders SET status = ? WHERE id = ?", (new_value, id))

                    # Сохранение изменений в базе данных
                    con.commit()
                    print("Заказ успешно изменен!")
                else:
                    print("Неверный выбор. Попробуйте еще раз.")
            else:
                print("Неверный выбор. Попробуйте еще раз.")

    con.close()
def theforgingdwarfuser():
    con = connect_database()
    cur = con.cursor()
    while True:
        print('Добро пожаловать в кузницу The Forging Dwarf!')
        print('Выберите одну из опций: ')
        print('1 - зарегестрироваться как клиент')
        print('2 - отправить заявку на заказ')
        print('3 - поиск')
        print('4 - вывести каталог изделий')
        number = int(input("Выберите для продолжения: "))
        #добавить себя как клиента
        if number == 1:
            con = connect_database()
            cur = con.cursor()
            lastname = input("Введите фамилию: ")
            firstname = input("Введите имя: ")
            address = input("Введите адрес: ")
            cur.execute("INSERT INTO clients (last_name, first_name, address) VALUES (?, ?, ?)",
                        (lastname, firstname, address))
            con.commit()
            print('Клиент успешно добавлен! ')
        #добавить заказ как клиент
        elif number == 2:
            firstname = input("Введите имя: ")
            lastname = input("Введите фамилию: ")
            cur.execute("SELECT id FROM clients WHERE first_name = ? AND last_name = ?", (firstname, lastname))
            client_rows = cur.fetchall()
            if len(client_rows) > 1:
                #если клиентов одинаковых несколько
                print("Найдено несколько клиентов с одинаковыми именем и фамилией, пожалуйста, укажите адрес.")
                address = input("Введите адрес: ")

                cur.execute("SELECT id FROM clients WHERE first_name = ? AND last_name = ? AND address = ?",
                            (firstname, lastname, address))
                client_id = cur.fetchone()
                if client_id is None:
                    print(
                        "Клиент с таким именем и адресом не найден, необходима регистрация. Желаете провести ее сейчас? (y/n)")
                    choice = input()
                    if choice == 'y':
                        con = connect_database()
                        cur = con.cursor()
                        lastname = input("Введите фамилию: ")
                        firstname = input("Введите имя: ")
                        address = input("Введите адрес: ")
                        cur.execute("INSERT INTO clients (last_name, first_name, address) VALUES (?, ?, ?)",
                                    (lastname, firstname, address))
                        con.commit()
                        print('Клиент успешно добавлен! ')
                        client_id = cur.lastrowid
                    else:
                        print("Без регистрации невозможно оформить заказ.")
                        break

                else:
                    client_id = client_id
            elif len(client_rows) == 1:
               client_id = client_rows[0][0]
            #такой клиент не найден
            if not client_rows:
                print("Клиент с таким именем не найден, необходима регистрация. Желаете провести ее сейчас? (y/n)")
                choice = input()
                if choice == 'y':
                    con = connect_database()
                    cur = con.cursor()
                    lastname = input("Введите фамилию: ")
                    firstname = input("Введите имя: ")
                    address = input("Введите адрес: ")
                    cur.execute("INSERT INTO clients (last_name, first_name, address) VALUES (?, ?, ?)",
                                (lastname, firstname, address))
                    con.commit()
                    print('Клиент успешно добавлен! ')
                    client_id = cur.lastrowid
                else:
                    print("Без регистрации невозможно оформить заказ.")
                    break

            else:
                client_id = client_id
            #оформление заказа как клиент
            choice = input("Выберите тип заказа: индивидуальный или из каталога? (i или c) ")
            if choice == 'i':
                req = input("Введите описание заказа: ")
                production_time = random.randint(350,1000)
                amount = input("Введите количество изделий: ")
                status = 'ip'
                created_at = datetime.datetime.now()
                cur.execute(
                    "INSERT INTO individual_orders (client_id, req, created_at, production_time, amount, status) VALUES (?, ?, ?, ?, ?, ?)",
                    (client_id, req, created_at, production_time, amount, status))
            elif choice == 'c':
                print('Список изделий из каталога: ')
                cur.execute("SELECT   *   FROM catalog")
                desc = cur.description
                headers = [col[0] for col in desc]
                print(headers)
                for row in cur:
                    print(row)
                catalog_id = input("Введите id изделия из каталога: ")
                cur.execute("SELECT production_time FROM catalog WHERE id = ?", (catalog_id,))
                production_time = cur.fetchone()[0]
                amount = input("Введите количество изделий: ")
                status = 'ip'
                created_at = datetime.datetime.now()
                cur.execute(
                    "INSERT INTO orders (client_id, catalog_id, created_at, production_time, amount, status) VALUES (?, ?, ?, ?, ?, ?)",
                    (client_id, catalog_id, created_at, production_time, amount, status))

            con.commit()
            print('Заказ успешно добавлен!')
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
add_data()
hashing_passwords()
authorization()



# cur.close()
#con.close()
