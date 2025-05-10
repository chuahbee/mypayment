import sqlite3

# 根据你数据库的位置调整路径！
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn
