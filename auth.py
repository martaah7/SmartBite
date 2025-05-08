import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        database='healthApp',
        user='root',
        password='Demonassassin2$'
    )

def get_user(username: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users WHERE Username=%s", (username,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

def verify_password(plain: str, stored: str) -> bool:
    # direct string compare
    return plain == stored

def create_user(username: str, password: str, role: str='customer', created_by: int=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Users (Username, Password, Role, Created_By) VALUES (%s,%s,%s,%s)",
        (username, password, role, created_by)
    )
    conn.commit()
    cursor.close()
    conn.close()

def change_password(username: str, old_password: str, new_password: str) -> bool:
    user = get_user(username)
    if not user or user['Password'] != old_password:
        return False
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET Password=%s WHERE User_ID=%s",
                   (new_password, user['User_ID']))
    conn.commit()
    cursor.close()
    conn.close()
    return True
