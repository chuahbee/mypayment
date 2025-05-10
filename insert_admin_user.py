from passlib.hash import sha256_crypt
import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

username = "admin"
password = "admin123"
hashed_password = sha256_crypt.hash(password)

cursor.execute("INSERT INTO admin_user (username, password, email) VALUES (?, ?, ?)",
               (username, hashed_password, "admin@example.com"))
conn.commit()
conn.close()

print("✅ 插入成功（密码已加密）")

