import sqlite3



def startdb():
    global conn, cursor
    conn = sqlite3.connect('data_heart.db')
    cursor = conn.cursor()

def create_tables():
    cursor.execute("CREATE TABLE IF NOT EXISTS user_id(id, name)")
    cursor.execute("CREATE TABLE IF NOT EXISTS user_attr(id, subreddits)")

def append_to_userID(id, redditor_name):
    cursor.execute("INSERT INTO user_id(id, name) VALUES(?, ?)",(id,redditor_name))
    conn.commit()

def append_to_userAttr(id, subs):
    cursor.execute("INSERT INTO user_attr(id, subreddits) VALUES(?,?)",(id,subs))
    conn.commit()

def closedb():
    cursor.close()
    conn.close()
