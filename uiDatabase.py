import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox, scrolledtext

class DBApp:
    def __init__(self, root, connection):
        self.root = root
        self.root.title("Customer Management")
        self.connection = connection

        self.label = tk.Label(root, text="Connected", font=("Arial", 20), fg="green")
        self.label.pack(pady=10)

        tk.Button(root, text="Close Connection", command=self.close_connection).pack(pady=2)

        '''
        Insert
        '''
        insert_section = tk.LabelFrame(root, text="Insert New Customer to Database", padx = 15, pady=15)
        insert_section.pack(pady=5, fill="x")
        
        self.entries = {}
        fields = [
            ("Customer_ID", "int"),
            ("CName", "str"),
            ("Dietary_Preference", "str"),
            ("Contact_Info", "str"),
            ("Payment_Info", "str"),
            ("Expenses", "float"),
            ("Nutritional_Info", "str")
        ]

        for field, _ in fields:
            #frame = tk.Frame(root)
            frame = tk.Frame(insert_section)
            frame.pack()
            tk.Label(frame, text=field+":", width=18, anchor="w").pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=30)
            entry.pack(side=tk.LEFT)
            self.entries[field] = entry

        #tk.Button(root, text="Insert", command=self.insert_customer).pack(pady=3)
        #tk.Button(root, text="Update", command=self.update_customer).pack(pady=3)
        #tk.Button(root, text="Delete", command=self.delete_customer).pack(pady=3)
        #tk.Button(root, text="Display Customers", command=self.display_customers).pack(pady=3)
        btn_frame_insert = tk.Frame(insert_section)
        btn_frame_insert.pack(pady=3)
        tk.Button(btn_frame_insert, text="Insert", width=15, command=self.insert_customer).pack(side=tk.LEFT, padx=5)
        

        '''
        Delete
        '''
        delete_frame = tk.LabelFrame(root, text="Delete Customer from Database", padx=15, pady=15)
        delete_frame.pack(pady=5, fill="x")

        self.delete_entries = {}
        delete_fields = [("Customer_ID", "int"), ("CName", "str")]

        for field, _ in delete_fields:
            frame = tk.Frame(delete_frame)
            frame.pack(fill="x")
            tk.Label(frame, text=field+":", width=18, anchor="w").pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=30)
            entry.pack(side=tk.LEFT)
            self.delete_entries[field] = entry

        btn_frame_delete = tk.Frame(delete_frame)
        btn_frame_delete.pack(pady=3)
        tk.Button(btn_frame_delete, text="Delete", width=15, command=self.delete_customer).pack(side=tk.LEFT, padx=5)
        #tk.Button(btn_frame1, text="Delete", width=15, command=self.delete_customer).pack(side=tk.LEFT, padx=5)

        btn_frame2 = tk.Frame(root)
        btn_frame2.pack(pady=3)

        tk.Button(btn_frame2, text="Update", width=15, command=self.update_customer).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame2, text="Display Customers", width=20, command=self.display_customers).pack(side=tk.LEFT, padx=5)


        self.text_area = scrolledtext.ScrolledText(root, width=70, height=10)
        self.text_area.pack(pady=5)
        self.text_area.config(state='disabled')

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.label.config(text="Disconnected", fg="red")

    def insert_customer(self):
        try:
            if not all(self.entries[field].get() for field in self.entries):
                messagebox.showwarning("Input Error", "All fields must be filled out.")
                return

            try:
                int(self.entries["Customer_ID"].get())
            except ValueError:
                messagebox.showwarning("Input Error", "Customer_ID must be an integer.")
                return

            try:
                float(self.entries["Expenses"].get())
            except ValueError:
                messagebox.showwarning("Input Error", "Expenses must be a number.")
                return
            
            data = self.get_entry_data()
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO Customers (Customer_ID, CName, Dietary_Preference, Contact_Info, Payment_Info, Expenses, Nutritional_Info)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, data)
            self.connection.commit()
            messagebox.showinfo("Success", "Customer inserted.")
        except Error as e:
            messagebox.showerror("Insert Error", str(e))

    def update_customer(self):
        try:
            data = self.get_entry_data()
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE Customers SET 
                    CName=%s,
                    Dietary_Preference=%s,
                    Contact_Info=%s,
                    Payment_Info=%s,
                    Expenses=%s,
                    Nutritional_Info=%s
                WHERE Customer_ID=%s
            """, (data[1], data[2], data[3], data[4], data[5], data[6], data[0]))
            self.connection.commit()
            messagebox.showinfo("Success", "Customer updated.")
        except Error as e:
            messagebox.showerror("Update Error", str(e))

    def delete_customer(self):
        try:
            customer_id = self.entries["Customer_ID"].get()
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM Customers WHERE Customer_ID = %s", (customer_id,))
            self.connection.commit()
            messagebox.showinfo("Success", "Customer deleted.")
        except Error as e:
            messagebox.showerror("Delete Error", str(e))

    def display_customers(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Customers")
            rows = cursor.fetchall()
            self.text_area.config(state='normal')
            self.text_area.delete('1.0', tk.END)
            self.text_area.insert(tk.END, "Customer_ID | CName | Dietary_Preference | Contact_Info | Payment_Info | Expenses | Nutritional_Info\n")
            self.text_area.insert(tk.END, "-" * 120 + "\n")
            for row in rows:
                line = " | ".join(str(col) for col in row)
                self.text_area.insert(tk.END, line + "\n")
            self.text_area.config(state='disabled')
        except Error as e:
            messagebox.showerror("Display Error", str(e))

    def get_entry_data(self):
        return tuple(self.entries[field].get() for field in [
            "Customer_ID", "CName", "Dietary_Preference", "Contact_Info",
            "Payment_Info", "Expenses", "Nutritional_Info"
        ])

class LoginWindow:
    def __init__(self):
        self.login_root = tk.Tk()
        self.login_root.title("MySQL Login")
        tk.Label(self.login_root, text="Enter MySQL Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.login_root, show="*")
        self.password_entry.pack(pady=5)
        tk.Button(self.login_root, text="Connect", command=self.try_connect).pack(pady=5)
        self.login_root.geometry("300x150")
        self.login_root.mainloop()

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
                app = DBApp(main_root, connection)
                main_root.geometry("700x600")
                main_root.mainloop()
        except Error as e:
            messagebox.showerror("Connection Failed", f"Error: {e}")

if __name__ == "__main__":
    LoginWindow()
