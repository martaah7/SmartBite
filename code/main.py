import tkinter as tk
from mysql.connector import connect, Error
from uiDatabase import DBAppCustomer

def connect_to_db():
    try:
        connection = connect(
            host="localhost",
            user="root",
            password="Wangzai!1",
            database="healthApp"
        )
        return connection
    except Error as e:
        print("Failed to connect to DB:", e)
        return None

def main():
    conn = connect_to_db()
    if not conn:
        return

    root = tk.Tk()
    root.title("SmartBites")
    
    app = DBAppCustomer(root, conn)
    
    root.mainloop()

if __name__ == "__main__":
    main()