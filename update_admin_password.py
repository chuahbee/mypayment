from passlib.hash import sha256_crypt
import sqlite3

db = sqlite3.connect("database.db")
hashed_password = sha256_crypt.hash("admin123")

db.execute("UPDATE admin_user SET password = ? WHERE username = ?", (hashed_password, "admin"))
db.commit()
db.close()

print("✅ 密码已加密并更新成功")
