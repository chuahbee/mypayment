import sqlite3
from passlib.hash import sha256_crypt

# 加密密码
hashed_password = sha256_crypt.hash("admin123")

# 连接数据库
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# 插入默认管理员账户
cursor.execute("""
    INSERT INTO admin_user (username, password, email)
    VALUES (?, ?, ?)
""", ("admin", hashed_password, "admin@example.com"))

conn.commit()
conn.close()

print("✅ 插入成功：用户名：admin，密码：admin123")
