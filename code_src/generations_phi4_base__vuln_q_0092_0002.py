import sqlite3

def delete_user_account(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()
    
    conn.close()