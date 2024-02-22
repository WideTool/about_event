import sqlite3

db = sqlite3.connect('db.db', check_same_thread=False)
cursor = db.cursor()

class User:
    def reg(user_id, full_name):
        cursor.execute(f"INSERT INTO users VALUES (id, full_name)", (user_id, full_name,))
        db.commit()

    def check_user(user_id):
        cursor.execute(f"SELECT id FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()

class Admin:
    def add_event(theme, description, photo_path, event_number):
        cursor.execute(f"INSERT INTO events VALUES (?, ?, ?, ?)", (theme, description, photo_path, event_number,))
        db.commit()
    
    def get_events():
        cursor.execute(f"SELECT * FROM events")
        events = cursor.fetchall()
        return events
    
    def get_last_event():
        cursor.execute(f"SELECT * FROM events ORDER BY event_number DESC LIMIT 1")
        return cursor.fetchone()
    
    def get_next_event_number():
        cursor.execute(f"SELECT * FROM events")
        return len(cursor.fetchall()) + 1

    def edit_event(event_number, theme, description, photo_path):
        cursor.execute(f"UPDATE events SET theme=?, description=?, photo_path=? WHERE event_number=?", (theme, description, photo_path, event_number, ))
        db.commit()

    def edit_event_by_number(event_number, theme, description, photo_path):
        cursor.execute(f"UPDATE events SET theme=?, description=?, photo_path=? WHERE event_number=?", (theme, description, photo_path, event_number,))
        db.commit()

    def clear_events():
        cursor.execute(f"DELETE FROM events")
        db.commit()