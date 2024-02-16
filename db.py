import sqlite3
import os

db = sqlite3.connect('about_event/db.db', check_same_thread=False)
cursor = db.cursor()

class User:
    def reg(user_id, full_name):
        cursor.execute(f"INSERT INTO users VALUES (id, full_name)", (user_id, full_name,))
        db.commit()

    def check_user(user_id):
        cursor.execute(f"SELECT id FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()

class Admin:
    def add_event(title, description):
        cursor.execute(f"INSERT INTO events VALUES (title, description)", (title, description,))
        db.commit()
    
    def clear_events():
        cursor.execute(f"DELETE FROM events")
        db.commit()
    
class Сonference:
    def events(day):
        cursor.execute(f"SELECT * FROM events WHERE day=?", (day,))
        return cursor.fetchall()