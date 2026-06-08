from app.database import get_connection
from app.security import hash_password

password = "change_me"

conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    "INSERT OR IGNORE INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)",
    ("admin", hash_password(password), 1)
)

conn.commit()
conn.close()

print("Admin created")