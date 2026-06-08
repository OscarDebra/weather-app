import os

DB_PATH = os.getenv("DB_PATH")

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print("DB deleted")

from database import init_db
init_db()

print("DB recreated")