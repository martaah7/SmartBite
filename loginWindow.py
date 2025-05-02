import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk

from customUIElements import ScrollableFrame
from uiDatabase import DBApp, DBAppCustomer

class LoginWindow:
    def __init__(self):
        self.login_root = tk.Tk()
        self.login_root.title("MySQL Login")
        
        tk.Label(self.login_root, text="Select Role:").pack(pady=5)
        self.user_type = tk.StringVar(value="Customer")
        tk.Button(self.login_root, text="Customer", command=self.set_user_as_customer).pack(pady=5)
        tk.Button(self.login_root, text="Employee", command=self.set_user_as_employee).pack(pady=5)

        self.login_root.geometry("300x150")
        self.login_root.mainloop()

    def set_user_as_customer(self):
        self.user_type = "Customer"
        self.ask_for_login()

    def set_user_as_employee(self):
        self.user_type = "Employee"
        self.ask_for_login()

    def ask_for_login(self):
        for widget in self.login_root.winfo_children():
            widget.destroy()

        ttk.Label(self.login_root, text="Enter MySQL Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.login_root, show="*")
        self.password_entry.pack(pady=5)
        tk.Button(self.login_root, text="Connect", command=self.try_connect_customer).pack(pady=5)
        
    def try_connect_customer(self):
        password = self.password_entry.get()
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='healthApp',
                user='root',
                password=password
            )
            if connection.is_connected():
                self.login_root.destroy()
                main_root = tk.Tk()
                main_root.title("Customer Management")
                main_root.geometry("700x600")

                scrollable_area = ScrollableFrame(main_root)
                scrollable_area.pack(fill="both", expand=True)
                
                app = DBAppCustomer(scrollable_area.scrollable_frame, connection)
                main_root.mainloop()
        except Error as e:
            messagebox.showerror("Connection Failed", f"Error: {e}")
    
    def try_connect(self):
        password = self.password_entry.get()
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='healthApp',
                user='root',
                password=password
            )
            if connection.is_connected():
                self.login_root.destroy()
                main_root = tk.Tk()
                main_root.title("Customer Management")
                main_root.geometry("700x600")

                scrollable_area = ScrollableFrame(main_root)
                scrollable_area.pack(fill="both", expand=True)
                
                app = DBApp(scrollable_area.scrollable_frame, connection)
                main_root.mainloop()
        except Error as e:
            messagebox.showerror("Connection Failed", f"Error: {e}")

#CSD@mysql-1872
if __name__ == "__main__":
    LoginWindow()
