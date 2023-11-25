import sqlite3

con = sqlite3.connect('data.sqlite')
cur = con.cursor()

#initializing tables
try:
    cur.execute("CREATE TABLE food(food_id INTEGER PRIMARY KEY AUTOINCREMENT, food_name TEXT, price REAL, cafe_location TEXT)")
except(sqlite3.OperationalError):
    print("DATABASE: Table food is already created")

try:
    cur.execute("CREATE TABLE customer_order(order_id INTEGER PRIMARY KEY AUTOINCREMENT, food_id, total_price FLOAT, FOREIGN KEY(food_id) REFERENCES food(food_id))")
except(sqlite3.OperationalError):
    print("DATABASE: Table customer_order is already created")

try:
    cur.execute("CREATE TABLE chosen_mahallah(chosen_mahallah)")
except:
    print("DATABASE: Table chosen_mahallah has been created")

try:
    cur.execute("CREATE TEMPORARY VIEW faruq_food AS SELECT * FROM food WHERE cafe_mahallah = 'faruq'")
except:
    print("DATABASE: View faruq_food is already created")

try:
    cur.execute("CREATE TEMPORARY VIEW faruq_food AS SELECT * FROM food WHERE cafe_mahallah = 'uthman'")
except:
    print("DATABASE: View uthman_food is already created")

try:
    cur.execute("CREATE TEMPORARY VIEW faruq_food AS SELECT * FROM food WHERE cafe_mahallah = 'siddiq'")
except:
    print("DATABASE: View siddiq_food is already created")

try:
    cur.execute("CREATE TEMPORARY VIEW faruq_food AS SELECT * FROM food WHERE cafe_mahallah = 'ali'")
except:
    print("DATABASE: view ali_food is already created")

try:
    cur.execute("CREATE TEMPORARY VIEW faruq_food AS SELECT * FROM food WHERE cafe_mahallah = 'bilal'")
except:
    print("DATABASE: view bilal_food is already created")

try:
    cur.execute("CREATE TEMPORARY VIEW faruq_food AS SELECT * FROM food WHERE cafe_mahallah = 'zubair'")
except:
    print("DATABASE: view zubair_food is already created")

def add_row(table, data):
    query = f'INSERT INTO {table} VALUES(?, ?, ?, ?)'
    cur.executemany(query, (data,))
    con.commit()
    print(f"DATABASE: New row has been added at table {table} {data}")

def read_table(table):
    query = f'SELECT * FROM {table}'
    res = cur.execute(query).fetchall()
    print(f"DATABASE: Returning all rows from table {table}")

    return res

def read_mahallah_food(mahallah:str):
    mahallah = mahallah.strip()
    query = f'SELECT * FROM food WHERE cafe_location = "{mahallah}"'
    res = cur.execute(query).fetchall()
    print(f"DATABASE: Returning all rows where cafe_location = '{mahallah}'")

    return res

def delete_all_row(table):
    query = f'DELETE FROM {table}'
    cur.execute(query)
    con.commit()
    print(f"All row in table{table} has been successfully delete")

def add_row_chosen_mahallah(table, data):
    query = f'INSERT INTO {table} VALUES(?)'
    cur.execute(query, (data,))
    con.commit()
    print("Successfully insert new Mahallah cafe for today")
