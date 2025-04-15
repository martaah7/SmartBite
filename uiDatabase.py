import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox, scrolledtext

class DBApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Management")
        self.connection = None

        self.label = tk.Label(root, text="Not Connected", font=("Arial", 20), fg="red")
        self.label.pack(pady=10)

        tk.Button(root, text="Open Connection", command=self.open_connection).pack(pady=2)
        tk.Button(root, text="Close Connection", command=self.close_connection).pack(pady=2)

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
            frame = tk.Frame(root)
            frame.pack()
            tk.Label(frame, text=field+":", width=18, anchor="w").pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=30)
            entry.pack(side=tk.LEFT)
            self.entries[field] = entry

        tk.Button(root, text="Insert", command=self.insert_customer).pack(pady=3)
        tk.Button(root, text="Update", command=self.update_customer).pack(pady=3)
        tk.Button(root, text="Delete", command=self.delete_customer).pack(pady=3)
        tk.Button(root, text="Display Customers", command=self.display_customers).pack(pady=3)

        self.text_area = scrolledtext.ScrolledText(root, width=70, height=10)
        self.text_area.pack(pady=5)
        self.text_area.config(state='disabled')

    def open_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='healthApp',
                user='root',
                password=''  # Replace with your MySQL password
            )
            if self.connection.is_connected():
                self.label.config(text="Connected", fg="green")
        except Error as e:
            messagebox.showerror("Connection Error", f"Error: {e}")

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.label.config(text="Disconnected", fg="red")

    def insert_customer(self):
        try:
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

if __name__ == "__main__":
    root = tk.Tk()
    app = DBApp(root)
    root.geometry("700x600")
    root.mainloop()
