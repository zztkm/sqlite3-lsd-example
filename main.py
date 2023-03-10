import sqlite3
from Levenshtein import distance

create_table_sql = """
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name STRING
    )
"""

con = sqlite3.connect(":memory:")
con.create_function("lsd", 2, distance)

cur = con.cursor()
cur = cur.execute(create_table_sql)
cur.execute('INSERT INTO user(name) VALUES("藤波 辰爾")')
cur.execute('INSERT INTO user(name) VALUES("ジャンボ鶴田")')
cur.execute('SELECT * FROM user')
print("all data")
print(cur.fetchall())
cur.close()

cur = con.cursor()
print()
print("lsd check data")
cur.execute('SELECT * FROM user WHERE lsd(name, "ジャンボ重田") < 3')

print(cur.fetchall())

con.close()
