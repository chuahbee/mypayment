import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()
#test
# 获取 admin_user 表结构
cursor.execute("PRAGMA table_info(admin_user);")
columns = cursor.fetchall()

print("🧾 admin_user 表结构：")
for col in columns:
    print(f"- {col[1]} ({col[2]})")

conn.close()
