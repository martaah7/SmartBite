import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk

class ScrollableFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class ExpandableItem(tk.Frame):
    def __init__(self, master, connection, item_name, item_type, *args, font_size = 14, can_edit = True, args_order = ["Description", "Expected Price", "Cooking Instructions", "Nutritional Info"], use_args_order = True, **kwargs):
        super().__init__(master, **kwargs)
        self.expanded = False
        self.detail_frame = None
        self.attributes = args
        self.can_edit = can_edit
        self.args_order = args_order
        self.use_args_order = use_args_order
        self.item_type = item_type
        self.item_name = item_name
        self.connection = connection

        #print(self.attributes)

        self.button = tk.Button(self, 
            text=item_name, 
            font=("Arial", font_size), 
            width=30,
            relief="flat",       
            borderwidth=0,anchor="w", 
            command=self.toggle_details)
        self.button.pack(fill="x")

    def toggle_details(self):
        if self.expanded:
            self.detail_frame.destroy()
            self.expanded = False
        else:
            self.detail_frame = tk.Frame(self, bg="#f0f0f0", padx=10, pady=5)

            for i, arg in enumerate(self.attributes):

                if i < len(self.args_order):
                    s = ""
                    if self.use_args_order:
                       s += self.args_order[i] + ":"

                    tk.Label(self.detail_frame, text=f"{s} {arg}", anchor="w").pack(fill="x")
                else:
                    w = ExpandableItem(self.detail_frame, self.connection, arg[0], self.item_type, *(arg[1:]), font_size=10, use_args_order=False)
                    w.pack(fill="x")
            #tk.Label(self.detail_frame, text=f"Price: ${self.price}", anchor="w").pack(fill="x")

            if self.can_edit:
                tk.Button(self.detail_frame, text="Edit", command=self.edit_item).pack(anchor="e", pady=5)
            self.detail_frame.pack(fill="x")
            self.expanded = True

    def edit_item(self):
        new_window = tk.Toplevel(self.master)
        new_window.title("Edit item")

        #print(self.attributes)

        for i, arg in enumerate(self.attributes):
                if i < len(self.args_order):
                    s = ""
                    if self.use_args_order:
                       s += self.args_order[i] + ":"

                    l = tk.Label(new_window, text=f"{s}", anchor="w").grid(row=i, column=0, padx=10, pady=5)
                    e = tk.Entry(new_window)
                    e.insert(0, self.attributes[i])
                    e.grid(row=i, column=1, padx=10, pady=5)

        def submit_edit():
            entries = [child for child in new_window.winfo_children() if isinstance(child, tk.Entry)]
            results = [entry.get() for entry in entries]

            #TODO: send querry to alter/edit entry in database
            edit_query = "UPDATE " + self.item_type + " AS " + self.item_type[0] + " SET "
            for i,result in enumerate(results):
                r = result
                if isinstance(result, str):
                    f = self.args_order[i]
                    if f == "Description":
                        f = self.item_type[0] + f

                    try:
                        r = int(result)
                        r = result
                    except ValueError:
                        r = "'" + result + "'"
                edit_query += self.item_type[0] + "." + f.replace(" ", "_") + " = " + r + ", "
            edit_query = edit_query[:-2]
            edit_query += " WHERE " + self.item_type[0] + "." + self.item_type[0] + "NAME = '" + self.item_name + "';"
            #print("edit querry:", edit_query)

            cursor = self.connection.cursor()
            cursor.execute(edit_query)

            self.connection.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Customer updated successfully.")
                #for entry in self.update_entries.values():
                #    entry.delete(0, tk.END)

                # Step 1: Refresh self.attributes from the DB
                refreshed_query = f"SELECT * FROM {self.item_type} WHERE {self.item_type[0]}NAME = %s;"
                cursor.execute(refreshed_query, (self.item_name,))
                row = cursor.fetchone()
                if row:
                    if self.item_type == "Recipe":
                        self.attributes = (row[3], row[5], row[2], row[4], self.attributes[4])  
                    
                    # Re-render detail_frame if expanded
                    if self.expanded:
                        self.detail_frame.destroy()
                        self.expanded = False
                        self.toggle_details()

                new_window.destroy()
            else:
                messagebox.showinfo("No Change", "No customer was updated.") 
            

        submit_edit_button = tk.Button(new_window, text="Save Edits", command=submit_edit)
        submit_edit_button.grid(row=len(self.args_order) + 1, column=1, padx=10, pady=5)
