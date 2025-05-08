import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk, simpledialog

from customUIElements import ScrollableFrame
from uiDatabase import DBApp, DBAppCustomer, DBAppAdmin
import auth

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HealthApp Login")
        tk.Label(self.root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.root); self.username_entry.pack()
        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*"); self.password_entry.pack()
        tk.Button(self.root, text="Login", command=self.try_login).pack(pady=10)
        tk.Button(self.root, text="Sign Up", command=self.sign_up).pack()
        self.root.mainloop()

    def try_login(self):
        uname = self.username_entry.get().strip()
        pw = self.password_entry.get()

        mysql_pw = simpledialog.askstring("MySQL password", "Enter your MySQL password:", show="*")
        if not mysql_pw:
            messagebox.showerror("Error", "No password provided.")
            return
        
        auth.set_mysql_password(mysql_pw)

        user = auth.get_user(uname)
        if not user or not auth.verify_password(pw, user['Password']):
            messagebox.showerror("Login Failed", "Invalid credentials.")
            return
        
        self.root.destroy()
        main = tk.Tk()
        role = user['Role']
        conn = auth.get_connection()

        if role == 'admin':
            app = DBAppAdmin(main, conn, user)
        elif role == 'employee':
            app = DBApp(main, conn)
        else:
            app = DBAppCustomer(main, conn, user)
        main.mainloop()


    def sign_up(self):
        """Allow any new customer to self-register."""
        win = tk.Toplevel(self.root)
        win.title("Sign Up")
        tk.Label(win, text="Username:").grid(row=0, column=0)
        e_user = tk.Entry(win); e_user.grid(row=0, column=1)
        tk.Label(win, text="Password:").grid(row=1, column=0)
        e_pw   = tk.Entry(win, show="*"); e_pw.grid(row=1, column=1)
        tk.Label(win, text="Confirm Password:").grid(row=2, column=0)
        e_pw2  = tk.Entry(win, show="*"); e_pw2.grid(row=2, column=1)

        def do_signup():
            u = e_user.get().strip()
            p = e_pw.get(); p2 = e_pw2.get()
            if not u or not p or p != p2:
                messagebox.showwarning("Error", "Must match and non-empty.")
                return
            
            mysql_pw = simpledialog.askstring("MySQL Password", "Enter your MySQL password:", show="*")
            if not mysql_pw:
                messagebox.showerror("Error", "No MySQL password provided.")
                return
            
            auth.set_mysql_password(mysql_pw)

            if auth.get_user(u):
                messagebox.showwarning("Error", "Username taken.")
                return

            auth.create_user(u, p, role='customer', created_by=None)
            messagebox.showinfo("Success", "Account created—you can now log in.")
            win.destroy()

        tk.Button(win, text="Create", command=do_signup).grid(row=3, column=1, pady=10)

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