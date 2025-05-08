import mysql.connector
import bcrypt

mysql_password = None

def set_mysql_password(pw):
    global mysql_password
    mysql_password = pw

def get_connection():
    if mysql_password is None:
        raise ValueError("MySQL password has not been set.")
    return mysql.connector.connect(
        host='localhost',
        database='healthApp',
        user='root',
        password=mysql_password
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
    try:
        return bcrypt.checkpw(plain.encode(), stored.encode())
    except Exception:
        return False

def create_user(username: str, password: str, role: str='customer', created_by: int=None):
    conn = get_connection()
    cursor = conn.cursor()

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    cursor.execute(
        "INSERT INTO Users (Username, Password, Role, Created_By) VALUES (%s,%s,%s,%s)",
        (username, hashed_pw, role, created_by)
    )
    conn.commit()
    cursor.close()
    conn.close()

def change_password(username: str, old_password: str, new_password: str) -> bool:
    user = get_user(username)
    if not user or not verify_password(old_password, user['Password']):
        return False

    conn = get_connection()
    cursor = conn.cursor()

    new_hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()

    cursor.execute("UPDATE Users SET Password=%s WHERE User_ID=%s",
                   (new_hashed_pw, user['User_ID']))
    conn.commit()
    cursor.close()
    conn.close()
    return True
