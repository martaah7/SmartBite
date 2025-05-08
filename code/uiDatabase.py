import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
from tkinter import ttk
import auth

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter

from customUIElements import ScrollableFrame, ExpandableItem, ItemType

class DBApp:
    def __init__(self, root, connection):
        self.root = root
        #self.root.title("Customer Management")
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

        '''
        Update
        '''
        update_frame = tk.LabelFrame(root, text="Update Existing Customer in Database", padx=15, pady=15)
        update_frame.pack(pady=5, fill="x")

        search_section = tk.Frame(update_frame)
        search_section.pack(fill="x")
        tk.Label(search_section, text="Customer ID to search:", width=18, anchor="w").pack(side=tk.LEFT)
        self.search_id_entry = tk.Entry(search_section, width=10)
        self.search_id_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_section, text="Search", command=self.search_customer).pack(side=tk.LEFT, padx=5)

        tk.Frame(update_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill="x", pady=10)

        self.update_entries = {}
        update_fields = [
            ("Customer_ID", "int"),
            ("CName", "str"),
            ("Dietary_Preference", "str"),
            ("Contact_Info", "str"),
            ("Payment_Info", "str"),
            ("Expenses", "float"),
            ("Nutritional_Info", "str")
        ]

        for field, _ in update_fields:
            frame = tk.Frame(update_frame)
            frame.pack(fill="x")
            tk.Label(frame, text=field + ":", width=18, anchor="w").pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=30)
            entry.pack(side=tk.LEFT)
            self.update_entries[field] = entry

        btn_frame_update = tk.Frame(update_frame)
        btn_frame_update.pack(pady=3)
        tk.Button(btn_frame_update, text="Update Customer", width=20, command=self.update_customer).pack(side=tk.LEFT, padx=5)
        
        btn_frame2 = tk.Frame(root)
        btn_frame2.pack(pady=3)

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
            customer_id = self.update_entries["Customer_ID"].get()
            if not customer_id:
                messagebox.showwarning("Input Error", "Customer ID is required for update.")
                return
                
            try:
                if self.update_entries["Expenses"].get():
                    float(self.update_entries["Expenses"].get())
            except ValueError:
                messagebox.showwarning("Input Error", "Expenses must be a number.")
                return
            
            data = (
                self.update_entries["CName"].get(),
                self.update_entries["Dietary_Preference"].get(),
                self.update_entries["Contact_Info"].get(),
                self.update_entries["Payment_Info"].get(),
                self.update_entries["Expenses"].get(),
                self.update_entries["Nutritional_Info"].get(),
                customer_id 
            )
            
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE Customers SET 
                    CName = %s,
                    Dietary_Preference = %s,
                    Contact_Info = %s,
                    Payment_Info = %s,
                    Expenses = %s,
                    Nutritional_Info = %s
                WHERE Customer_ID = %s
            """, data)
            
            self.connection.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Customer updated successfully.")
                for entry in self.update_entries.values():
                    entry.delete(0, tk.END)
            else:
                messagebox.showinfo("No Change", "No customer was updated.")        
        except Error as e:
            messagebox.showerror("Update Error", str(e))

    def search_customer(self):
        try:
            customer_id = self.search_id_entry.get()
            if not customer_id:
                messagebox.showwarning("Input Error", "Please enter a Customer ID to search.")
                return
                
            try:
                int(customer_id)
            except ValueError:
                messagebox.showwarning("Input Error", "Customer ID must be an integer.")
                return
                
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Customers WHERE Customer_ID = %s", (customer_id,))
            customer = cursor.fetchone()
            
            if customer:
                fields = ["Customer_ID", "CName", "Dietary_Preference", "Contact_Info",
                        "Payment_Info", "Expenses", "Nutritional_Info"]
                
                for field in fields:
                    self.update_entries[field].delete(0, tk.END)
                
                for i, field in enumerate(fields):
                    self.update_entries[field].insert(0, str(customer[i]))
                    
                self.update_button.config(state=tk.NORMAL)
                messagebox.showinfo("Customer Found", f"Customer {customer_id} found. You can now update their details.")
            else:
                messagebox.showinfo("Not Found", f"No customer found with ID: {customer_id}")
                for entry in self.update_entries.values():
                    entry.delete(0, tk.END)
                self.update_button.config(state=tk.DISABLED)
                    
        except Error as e:
            messagebox.showerror("Search Error", str(e))

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

class DBAppCustomer:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.customer_id = 1

        # Header label with green background
        header = tk.Label(root, text="SmartBite", bg="green", fg="white", font=("Arial", 24, "bold"))
        header.pack(fill="x")  # Fill the horizontal space


        self.label = tk.Label(root, text="Connected", font=("Arial", 20), fg="green")
        self.label.pack(pady=10)

        tk.Button(root, text="Close Connection", command=self.close_connection).pack(pady=2)

         # Tabbed interface
        tab_control = ttk.Notebook(root)
        tab_control.pack(expand=1, fill="both")

        # --- Tab 1: My Recipes/Meal Plans ---
        self.my_items_tab = tk.Frame(tab_control)
        tab_control.add(self.my_items_tab, text="My Items")
        self.display_my_items()

        self.saved_items_tab = tk.Frame(tab_control)
        tab_control.add(self.saved_items_tab, text="Saved Items")
        self.display_my_saved_items()

        # --- Tab 3: Friends/Following ---
        self.friends_tab = tk.Frame(tab_control)
        tab_control.add(self.friends_tab, text="Following")
        self.display_friends()

        # --- Tab 4: My Grocery List ---
        self.grocery_tab = tk.Frame(tab_control)
        tab_control.add(self.grocery_tab, text="My Grocery List")
        self.display_grocery_list()

        # Tab 5
        self.popular_recipes_tab = tk.Frame(tab_control)
        tab_control.add(self.popular_recipes_tab, text="Popular Recipes")
        self.display_popular_items(self.popular_recipes_tab, "Recipe")

        # Tab 6
        self.popular_meals_tab = tk.Frame(tab_control)
        tab_control.add(self.popular_meals_tab, text="Popular Meal Plans")
        self.display_popular_items(self.popular_meals_tab, "Meal Plan")

        # Tab 7
        self.my_reviews_tab = tk.Frame(tab_control)
        tab_control.add(self.my_reviews_tab, text="My Reviews")
        self.display_my_reviews()


    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.label.config(text="Disconnected", fg="red")

    '''--------------------------------------------------
    
        FUNCTIONS THAT POPULATE MAJOR TAB PAGES

    --------------------------------------------------'''
    '''
    Prefilled version
    '''
    def open_review_dialog_prefilled(self, review_type, item_id, item_name):
        dialog = tk.Toplevel(self.root)
        dialog.title("Leave a Review")

        # Review Type (not editable)
        tk.Label(dialog, text="Review Type:").grid(row=0, column=0)
        tk.Label(dialog, text=review_type).grid(row=0, column=1)

        # Item (not editable)
        tk.Label(dialog, text="Item:").grid(row=1, column=0)
        tk.Label(dialog, text=item_name).grid(row=1, column=1)

        # Rating
        tk.Label(dialog, text="Rating (1-5):").grid(row=2, column=0)
        rating_entry = tk.Entry(dialog)
        rating_entry.grid(row=2, column=1)

        # Review Text
        tk.Label(dialog, text="Review Text:").grid(row=3, column=0)
        text_entry = tk.Entry(dialog, width=40)
        text_entry.grid(row=3, column=1)

        def submit_review():
            try:
                rating = int(rating_entry.get())
                review_text = text_entry.get()
                if not (1 <= rating <= 5):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Input Error", "Invalid rating.")
                return

            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO ReviewRating (Customer_ID, Review_Type, Item_ID, Rating, RDescription) VALUES (%s, %s, %s, %s, %s)",
                (self.customer_id, review_type, item_id, rating, review_text)
            )
            self.connection.commit()
            messagebox.showinfo("Success", "Review submitted!")
            dialog.destroy()
            if review_type=="Recipe":
                self.refresh_popular_items_tab(self.popular_recipes_tab, "Recipe")
            else:
                self.refresh_popular_items_tab(self.popular_meals_tab, "Meal Plan")
            self.refresh_my_reviews_tab()

        tk.Button(dialog, text="Submit", command=submit_review).grid(row=4, column=1, pady=10)

    '''
    Displays all of the information under the My Grocery List tab
    '''
    def display_grocery_list(self):
        try:
            #Getting the user's grocery list
            cursor = self.connection.cursor()
            query = """
                SELECT * 
                FROM GroceryList 
                WHERE Customer_ID = %s"""

            cursor.execute(query, (self.customer_id,))
            rows = cursor.fetchall()

            query = """
                SELECT G.Nutritional_Info, I.* 
                FROM GroceryListItems AS GI
                JOIN GroceryList AS G ON G.List_ID = GI.List_ID
                JOIN Ingredient AS I ON GI.Ingredient_ID = I.Ingredient_ID 
                WHERE G.Customer_ID = %s"""
            cursor.execute(query, (self.customer_id,))
            list_items = cursor.fetchall()

            query = """
                SELECT G.List_ID
                FROM GroceryList AS G 
                WHERE G.Customer_ID = %s"""
            cursor.execute(query, (self.customer_id,))
            list_id = cursor.fetchall()[0][0]
            #print(rows)
            
            '''
            Grocery List UI
            '''
            #list of ingredients
            ingredient_frame = tk.Frame(self.grocery_tab)
            ingredient_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

            self.checkbox_vars = []
            
            
            def add_item_to_list():
                new_window = tk.Toplevel(self.root)
                new_window.title("Add item")

                query = """
                    SELECT * 
                    FROM INGREDIENT 
                    """
                cursor.execute(query)
                list_items = cursor.fetchall()
                #print(list_items)
                
                tk.Label(new_window, text="Select Item to Add:").grid(row=0, column=0)
                i_name = tk.StringVar()
                type_combo = ttk.Combobox(new_window, textvariable=i_name, values=[ingredient[1] for ingredient in list_items], state="readonly")
                type_combo.grid(row=0, column=1)

                def submit_add():
                    #entries = [child for child in new_window.winfo_children() if isinstance(child, tk.Entry)]
                    #results = [entry.get() for entry in entries]
                    ingredient_name = i_name.get() #results[0]
                    query = """
                        SELECT Ingredient_ID
                        FROM INGREDIENT
                        WHERE IName = %s 
                        """
                    cursor.execute(query, (ingredient_name,))
                    i_id = cursor.fetchall()
                    #print(i_id)

                    #print(results)

                    query = """
                        INSERT IGNORE INTO GroceryListItems (List_ID, Ingredient_ID)
                        VALUES (%s, %s)
                        """
                    cursor.execute(query, (list_id,i_id[0][0],))
                    self.connection.commit()

                    if cursor.rowcount > 0:
                        messagebox.showinfo("Success", "Grocery List updated successfully.")

                        query = """
                            SELECT * 
                            FROM Ingredient
                            WHERE Ingredient_ID = %s;
                            """
                        cursor.execute(query, (i_id[0][0],))
                        added_info = cursor.fetchall()[0]
                        #print(added_info)

                        query = """
                            SELECT G.Nutritional_Info, I.* 
                            FROM GroceryListItems AS GI
                            JOIN GroceryList AS G ON G.List_ID = GI.List_ID
                            JOIN Ingredient AS I ON GI.Ingredient_ID = I.Ingredient_ID 
                            WHERE G.Customer_ID = %s"""
                        cursor.execute(query, (self.customer_id,))
                        list_items = cursor.fetchall()

                        i = len(list_items)
                        tk.Label(ingredient_frame, text=added_info[0], font=("Arial", 12, "bold")).grid(row=i + 1, column=0, padx=5, pady=5, sticky="w")
                        tk.Label(ingredient_frame, text=added_info[1], font=("Arial", 12)).grid(row=i + 1, column=1, padx=5, pady=5, sticky="w")
                        tk.Label(ingredient_frame, text=added_info[4], font=("Arial", 12)).grid(row=i + 1, column=2, padx=5, pady=5, sticky="w")

                        #checkbox    
                        var = tk.BooleanVar()
                        checkbox = tk.Checkbutton(ingredient_frame, variable=var)
                        checkbox.grid(row=i + 1, column=3)
                        self.checkbox_vars.append(var)                     

                        new_window.destroy()
                    else:
                        messagebox.showinfo("No Change", "No ingredient was added.") 

                    new_window.destroy()
                    

                submit_add_button = tk.Button(new_window, text="Save Edits", command=submit_add)
                submit_add_button.grid(row=1, column=1, padx=10, pady=5)
             
            def write_header():
                # Header
                tk.Label(self.grocery_tab, text="My Grocery List", font=("Arial", 32, "bold")).grid(row=0, column=0, padx=(0,25), pady=5, sticky="w")
                tk.Label(self.grocery_tab, text="Expected Price Range: " + rows[0][2], font=("Arial", 16)).grid(row=0, column=1, padx=5, pady=5, sticky="e")
                tk.Label(self.grocery_tab, text="List Description: " + rows[0][3], font=("Arial", 12)).grid(row=1, column=1, padx=25, pady=5, sticky="e")
                
                tk.Label(self.grocery_tab, text="Ingredients", font=("Arial", 26, "bold")).grid(row=2, column=0, padx=5, pady=5, sticky="w")
                tk.Button(self.grocery_tab, text="Add Item  +", width=20, command=add_item_to_list).grid(row=2, column=1, padx=(0,25), pady=5, sticky="e")



                # Make the grocery_tab columns expand
                self.grocery_tab.grid_columnconfigure(0, weight=1)
                self.grocery_tab.grid_columnconfigure(1, weight=1)

                # Make ingredient_frame columns expand
                ingredient_frame.grid_columnconfigure(0, weight=1)
                ingredient_frame.grid_columnconfigure(1, weight=1)
                ingredient_frame.grid_columnconfigure(2, weight=1)
                ingredient_frame.grid_columnconfigure(3, weight=1)

                # Headers for ingredients
                tk.Label(ingredient_frame, text="ID", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
                tk.Label(ingredient_frame, text="Name", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5, pady=5, sticky="w")
                tk.Label(ingredient_frame, text="Price", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=5, pady=5, sticky="w")

            write_header()

            for i, item in enumerate(list_items):
                tk.Label(ingredient_frame, text=item[1], font=("Arial", 12, "bold")).grid(row=i + 1, column=0, padx=5, pady=5, sticky="w")
                tk.Label(ingredient_frame, text=item[2], font=("Arial", 12)).grid(row=i + 1, column=1, padx=5, pady=5, sticky="w")
                tk.Label(ingredient_frame, text=item[5], font=("Arial", 12)).grid(row=i + 1, column=2, padx=5, pady=5, sticky="w")

                #checkbox    
                var = tk.BooleanVar()
                checkbox = tk.Checkbutton(ingredient_frame, variable=var)
                checkbox.grid(row=i + 1, column=3)
                self.checkbox_vars.append(var)

            def remove_list_item():
                #entries = [child for child in ingredient_frame.winfo_children() if isinstance(child, tk.Checkbutton)]
                results = [var.get() for var in self.checkbox_vars]
                #print(results)

                for i, result in enumerate(results):
                    if result:
                        ingredient_id = -1
                        for widget in ingredient_frame.grid_slaves(row=i+1):
                            if isinstance(widget, tk.Label):
                                if widget.grid_info()["column"] == 0:
                                    ingredient_id = widget.cget('text')
                            widget.destroy()
                        
                        #write query to actually remove it from list
                        query = """
                            DELETE FROM GroceryListItems AS GI
                            WHERE GI.List_ID = %s AND GI.Ingredient_ID = %s"""

                        #print(list_id, ingredient_id)
                        if list_id > 0 and ingredient_id > 0:
                            cursor.execute(query, (list_id,ingredient_id,))
                            self.connection.commit()

            tk.Button(self.grocery_tab, text="Remove Items", width=20, command=remove_list_item).grid(row=4, column=0, columnspan=2, padx=(0,25), pady=5, sticky="ew")

        except Error as e:
            messagebox.showerror("Display Error", str(e))

    '''
    Displays all of the information under the My Items tab
    '''
    def display_my_items(self):
        try:
            #Getting the user's items list
            cursor = self.connection.cursor()
            r_query = "SELECT * FROM Recipe AS R WHERE R.Created_By = " + str(self.customer_id) 
            mp_query = "SELECT * FROM MealPlan AS MP WHERE MP.Created_By = " + str(self.customer_id)
            cursor.execute(r_query)
            r_rows = cursor.fetchall()
            
            cursor.execute(mp_query)
            mp_rows = cursor.fetchall()
            
            '''
            My Items UI
            '''
            # Header
            tk.Label(self.my_items_tab, text="My Created Items", font=("Arial", 32, "bold")).grid(row=0, column=0, padx=(0,25), pady=5, sticky="w")
            
            tk.Button(self.my_items_tab, text="Add Item  +", width=20, command=self.add_item).grid(row=0, column=1, padx=(0,25), pady=5, sticky="e")


            #list of items
            item_frame = tk.Frame(self.my_items_tab)
            item_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

            # Make the tab columns expand
            self.my_items_tab.grid_columnconfigure(0, weight=1)
            self.my_items_tab.grid_columnconfigure(1, weight=1)

            # Make frame columns expand
            item_frame.grid_columnconfigure(0, weight=1)
            item_frame.grid_columnconfigure(1, weight=1)
            item_frame.grid_columnconfigure(2, weight=1)
            item_frame.grid_columnconfigure(3, weight=1)

            # Headers for ingredients
            tk.Label(item_frame, text="Type", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
            tk.Label(item_frame, text="Name", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5, pady=5, sticky="w")
            
            for i, row in enumerate(r_rows):
                tk.Label(item_frame, text="Recipe", font=("Arial", 14)).grid(row=i+1, column=0, padx=5, pady=5, sticky="w")
                #tk.Label(item_frame, text=row[1], font=("Arial", 10)).grid(row=i+1, column=1, padx=5, pady=5, sticky="w")
                
                ri_query = """
                    SELECT I.* 
                    FROM RecipeIngredient AS RI 
                    JOIN Ingredient AS I ON RI.Ingredient_ID = I.Ingredient_ID
                    WHERE RI.Recipe_ID = %s"""
                cursor.execute(ri_query, (row[0],))
                ri_result = cursor.fetchall()
                #print("searchring for id:", row[0], "ri result:", ri_result)

                s = ["Ingredients"] + [row[1] for row in ri_result]
                #print(s)
                
                w = ExpandableItem(item_frame, self.connection, row[1], ItemType.RECIPE, row[3], row[5], row[2], row[4], s)
                w.grid(row=i+1, column=1, padx=5, pady=5, sticky="w")

            for i, row in enumerate(mp_rows):
                tk.Label(item_frame, text="Meal Plan", font=("Arial", 14)).grid(row=i+1 + len(r_rows), column=0, padx=5, pady=5, sticky="w")
                #tk.Label(item_frame, text=row[1], font=("Arial", 10)).grid(row=i+1 + len(r_rows), column=1, padx=5, pady=5, sticky="w")
                
                mr_query = """
                    SELECT R.* 
                    FROM MealPlanRecipe AS MR 
                    JOIN Recipe AS R ON MR.Recipe_ID = R.Recipe_ID
                    WHERE MR.MealPlan_ID = %s"""
                cursor.execute(mr_query, (row[0],))
                mr_result = cursor.fetchall()
                
                s = ["Recipes"] + [row[1] for row in mr_result]
                #print(s)

                w = ExpandableItem(item_frame, self.connection, row[1], ItemType.MEALPLAN, row[4], row[3], row[2], row[5], s)
                w.grid(row=i+1 + len(r_rows), column=1, padx=5, pady=5, sticky="w")

        except Error as e:
            messagebox.showerror("Display Error", str(e))

        '''
    Displays all of the information under the My Items tab
    '''
    
    '''
    Displays all the information under the saved items tab
    '''
    def display_my_saved_items(self):
        try:
            #Getting the user's items list
            cursor = self.connection.cursor()
            sr_query = """
                SELECT R.* 
                FROM RSavedBy AS RS
                JOIN Recipe AS R ON RS.ID = R.Recipe_ID
                WHERE RS.Customer_ID = %s"""
            cursor.execute(sr_query, (self.customer_id,))
            r_rows = cursor.fetchall()
            
            sm_query = """
                SELECT M.* 
                FROM MSavedBy AS MS
                JOIN MealPlan AS M ON MS.ID = M.Meal_Plan_ID
                WHERE MS.Customer_ID = %s"""
            cursor.execute(sm_query, (self.customer_id,))
            mp_rows = cursor.fetchall()
            
            '''
            My Items UI
            '''
            # Header
            tk.Label(self.saved_items_tab, text="My Saved Items", font=("Arial", 32, "bold")).grid(row=0, column=0, padx=(0,25), pady=5, sticky="w")

            #list of items
            item_frame = tk.Frame(self.saved_items_tab)
            item_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

            # Make the tab columns expand
            self.saved_items_tab.grid_columnconfigure(0, weight=1)
            self.saved_items_tab.grid_columnconfigure(1, weight=1)

            # Make frame columns expand
            item_frame.grid_columnconfigure(0, weight=1)
            item_frame.grid_columnconfigure(1, weight=1)
            item_frame.grid_columnconfigure(2, weight=1)
            item_frame.grid_columnconfigure(3, weight=1)

            # Headers for ingredients
            tk.Label(item_frame, text="Type", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
            tk.Label(item_frame, text="Name", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5, pady=5, sticky="w")
            
            for i, row in enumerate(r_rows):
                tk.Label(item_frame, text="Recipe", font=("Arial", 14)).grid(row=i+1, column=0, padx=5, pady=5, sticky="w")
                #tk.Label(item_frame, text=row[1], font=("Arial", 10)).grid(row=i+1, column=1, padx=5, pady=5, sticky="w")

                ri_query = """
                    SELECT I.* 
                    FROM RecipeIngredient AS RI 
                    JOIN Ingredient AS I ON RI.Ingredient_ID = I.Ingredient_ID
                    WHERE RI.Recipe_ID = %s"""
                cursor.execute(ri_query, (row[0],))
                ri_result = cursor.fetchall()
                #print("searchring for id:", row[0], "ri result:", ri_result)

                s = ["Ingredients"] + [row[1] for row in ri_result]
                #print(s)
                
                w = ExpandableItem(item_frame, self.connection, row[1], ItemType.RECIPE, row[3], row[5], row[2], row[4], s, can_edit=False)
                w.grid(row=i+1, column=1, padx=5, pady=5, sticky="w")
                original_toggle = w.toggle_details
                def new_toggle(orig=original_toggle, w=w, rid=row[0], name=row[1]):
                    orig()   # call built-in expand/collapse
                    if w.expanded:
                        # pack the button at bottom of detail_frame
                        tk.Button(
                            w.detail_frame,
                            text="Leave a Review",
                            command=lambda: self.open_review_dialog_prefilled("Recipe", rid, name)
                        ).pack(anchor="e", pady=5)
                w.toggle_details = new_toggle
                w.button.config(command=new_toggle)

            for i, row in enumerate(mp_rows):
                tk.Label(item_frame, text="Meal Plan", font=("Arial", 14)).grid(row=i+1 + len(r_rows), column=0, padx=5, pady=5, sticky="w")
                #tk.Label(item_frame, text=row[1], font=("Arial", 10)).grid(row=i+1 + len(r_rows), column=1, padx=5, pady=5, sticky="w")
                
                mr_query = """
                    SELECT R.* 
                    FROM MealPlanRecipe AS MR 
                    JOIN Recipe AS R ON MR.Recipe_ID = R.Recipe_ID
                    WHERE MR.MealPlan_ID = %s"""
                cursor.execute(mr_query, (row[0],))
                mr_result = cursor.fetchall()
                
                s = ["Recipes"] + [row[1] for row in mr_result]
                #print(s)

                w = ExpandableItem(item_frame, self.connection, row[1], ItemType.MEALPLAN, row[4], row[3], row[2], row[5], s, can_edit=False)
                w.grid(row=i+1 + len(r_rows), column=1, padx=5, pady=5, sticky="w")
                original_toggle = w.toggle_details
                def new_toggle(orig=original_toggle, w=w, mid=row[0], name=row[1]):
                    orig()
                    if w.expanded:
                        tk.Button(
                            w.detail_frame,
                            text="Leave a Review",
                            command=lambda: self.open_review_dialog_prefilled("MealPlan", mid, name)
                        ).pack(anchor="e", pady=5)
                w.toggle_details = new_toggle
                w.button.config(command=new_toggle)

        except Error as e:
            messagebox.showerror("Display Error", str(e))


    '''
    Displys all the friends information under the friends tab
    '''
    def display_friends(self):
        try:
            #Getting the user's friends
            cursor = self.connection.cursor()
            following_query = "SELECT * FROM CustomerFollows WHERE Follower_ID = " + str(self.customer_id) #WHERE R.Recipe_ID <= 10"
            cursor.execute(following_query)
            follower_rows = cursor.fetchall()
            following_ids = [f[1] for f in follower_rows]
            #print(following_ids)
            
            def follow_new():
                new_window = tk.Toplevel(self.root)
                new_window.title("Follow")

                query = """
                    SELECT * 
                    FROM CUSTOMERS
                    WHERE NOT Customer_ID = %s 
                    """
                cursor.execute(query, (self.customer_id,))
                customers = cursor.fetchall()
                #print(list_items)
                
                tk.Label(new_window, text="Select Account to Follow:    ").grid(row=0, column=0)
                f_name = tk.StringVar()
                type_combo = ttk.Combobox(new_window, textvariable=f_name, values=[customer[1] for customer in customers], state="readonly")
                type_combo.grid(row=0, column=1)
                
                def submit_add():
                    new_following_name = f_name.get()
                    query = """
                        SELECT Customer_ID
                        FROM CUSTOMERS
                        WHERE CName = %s 
                        """
                    cursor.execute(query, (new_following_name,))
                    f_id = cursor.fetchall()
                    #print(f_id)

                    query = """
                        INSERT IGNORE INTO CustomerFollows (Follower_ID, Followed_ID)
                        VALUES (%s, %s)
                        """
                    cursor.execute(query, (self.customer_id,f_id[0][0],))
                    self.connection.commit()

                    if cursor.rowcount > 0:
                        messagebox.showinfo("Success", f"Followed {new_following_name} successfully.")
                    else:
                        messagebox.showinfo("No Change", "No account was followed.") 

                    self.refresh_my_friends_tab()
                    new_window.destroy()
                    
                submit_add_button = tk.Button(new_window, text="Follow", command=submit_add)
                submit_add_button.grid(row=1, column=1, padx=10, pady=5)

            '''
            My Friends UI
            '''
            # Header
            tk.Label(self.friends_tab, text="My Friends", font=("Arial", 32, "bold")).grid(row=0, column=0, padx=(0,25), pady=5, sticky="w")
            tk.Button(self.friends_tab, text="Follow New Account  +", width=20, command=follow_new).grid(row=0, column=1, padx=(0,25), pady=5, sticky="e")

            #list of following
            following_frame = tk.Frame(self.friends_tab)
            following_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

            # Make the tab columns expand
            self.friends_tab.grid_columnconfigure(0, weight=1)
            self.friends_tab.grid_columnconfigure(1, weight=1)

            # Make frame columns expand
            following_frame.grid_columnconfigure(0, weight=1)
            following_frame.grid_columnconfigure(1, weight=1)
            following_frame.grid_columnconfigure(2, weight=1)
            following_frame.grid_columnconfigure(3, weight=1)

            # Headers for ingredients
            #tk.Label(following_frame, text="Type", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
            tk.Label(following_frame, text="Name", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
            
            for i, following_id in enumerate(following_ids):
                #tk.Label(following_frame, text="Recipe", font=("Arial", 14)).grid(row=i+1, column=0, padx=5, pady=5, sticky="w")
                #tk.Label(item_frame, text=row[1], font=("Arial", 10)).grid(row=i+1, column=1, padx=5, pady=5, sticky="w")
                
                cname_query = """
                    SELECT C.CName 
                    FROM Customers AS C 
                    WHERE C.Customer_ID = %s""" 
                cursor.execute(cname_query, (following_id,))
                cname_result = cursor.fetchall()
                #print("searchring for id:", row[0], "ri result:", ri_result)

                s = cname_result[0][0]
                #print(s)
            
                w = ExpandableItem(following_frame, self.connection, s, ItemType.CUSTOMER, following_id, can_edit=False, is_sub_item=True, customer_id=self.customer_id)
                w.grid(row=i+1, column=0, padx=5, pady=5, sticky="w")
      
        except Error as e:
            messagebox.showerror("Display Error", str(e))
        
        
    def add_item(self):
        """
        Opens a dialog to create a new Recipe or Meal Plan for the current customer,
        inserts it into the database, and refreshes the My Items tab.
        """
        new_window = tk.Toplevel(self.root)
        new_window.title("Add Item")
        
        # Select between adding a Recipe or a Meal Plan
        tk.Label(new_window, text="Select Type:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        type_var = tk.StringVar(value="Recipe")
        tk.Radiobutton(new_window, text="Recipe", variable=type_var, value="Recipe").grid(row=0, column=1, padx=5, pady=5)
        tk.Radiobutton(new_window, text="Meal Plan", variable=type_var, value="Meal Plan").grid(row=0, column=2, padx=5, pady=5)
        
        # Frame to hold the field entries
        fields_frame = tk.Frame(new_window)
        fields_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        
        # Define which labels to show for each type
        labels = {
            "Recipe": ["Name", "Description", "Instructions", "Nutritional Info", "Expected Price"],
            "Meal Plan": ["Name", "Duration (days)", "Expected Price", "Description", "Nutritional Info"]
        }
        entries = {}
        
        # Render the appropriate fields when type changes
        def render_fields(*args):
            for widget in fields_frame.winfo_children():
                widget.destroy()
            current = type_var.get()
            for i, label in enumerate(labels[current]):
                tk.Label(fields_frame, text=label+":", anchor="w").grid(row=i, column=0, padx=5, pady=5, sticky="w")
                e = tk.Entry(fields_frame, width=40)
                e.grid(row=i, column=1, padx=5, pady=5)
                entries[label] = e
        type_var.trace_add("write", render_fields)
        render_fields()
        
        # Handle submission of new item
        def submit():
            item_type = type_var.get()
            cursor = self.connection.cursor()
            if item_type == "Recipe":
                # Generate a new Recipe_ID
                cursor.execute("SELECT IFNULL(MAX(Recipe_ID),0)+1 FROM Recipe")
                new_id = cursor.fetchone()[0]
                data = (
                    new_id,
                    entries["Name"].get(),
                    entries["Instructions"].get(),
                    entries["Description"].get(),
                    entries["Nutritional Info"].get(),
                    int(entries["Expected Price"].get()),
                    self.customer_id,
                    False
                )
                cursor.execute(
                    """
                    INSERT INTO Recipe
                      (Recipe_ID, RName, Cooking_Instructions, RDescription,
                       Nutritional_Info, Expected_Price, Created_By, Is_Private_Visibility)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    """, data)
            else:
                # Generate a new MealPlan_ID
                cursor.execute("SELECT IFNULL(MAX(Meal_Plan_ID),0)+1 FROM MealPlan")
                new_id = cursor.fetchone()[0]
                data = (
                    new_id,
                    entries["Name"].get(),
                    int(entries["Duration (days)"].get()),
                    int(entries["Expected Price"].get()),
                    entries["Description"].get(),
                    entries["Nutritional Info"].get(),
                    self.customer_id,
                    False
                )
                cursor.execute(
                    """
                    INSERT INTO MealPlan
                      (Meal_Plan_ID, MName, Duration, Expected_Price,
                       MDescription, Nutritional_Info, Created_By, Is_Private_Visibility)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    """, data)
            self.connection.commit()
            messagebox.showinfo("Success", f"{item_type} added successfully.")
            # Refresh the My Items tab
            for widget in self.my_items_tab.winfo_children():
                widget.destroy()
            self.display_my_items()
            new_window.destroy()

        tk.Button(new_window, text="Add", command=submit).grid(row=2, column=1, pady=10)

    def display_popular_items(self, tab, item_type):
        cursor = self.connection.cursor()
        if item_type == "Recipe":
            query = """
                SELECT R.Recipe_ID, R.RName, R.RDescription, R.Expected_Price,
                       R.Cooking_Instructions, R.Nutritional_Info,
                       AVG(Rev.Rating) AS AvgRating, COUNT(Rev.Rating) AS NumReviews
                FROM Recipe AS R
                LEFT JOIN ReviewRating AS Rev
                  ON Rev.Item_ID = R.Recipe_ID AND Rev.Review_Type='Recipe'
                GROUP BY R.Recipe_ID
                ORDER BY NumReviews DESC, AvgRating DESC
                LIMIT 10
            """
        else:
            query = """
                SELECT M.Meal_Plan_ID, M.MName, M.MDescription, M.Expected_Price,
                       M.Duration, M.Nutritional_Info,
                       AVG(Rev.Rating) AS AvgRating, COUNT(Rev.Rating) AS NumReviews
                FROM MealPlan AS M
                LEFT JOIN ReviewRating AS Rev
                  ON Rev.Item_ID = M.Meal_Plan_ID AND Rev.Review_Type='MealPlan'
                GROUP BY M.Meal_Plan_ID
                ORDER BY NumReviews DESC, AvgRating DESC
                LIMIT 10
            """
        cursor.execute(query)
        items = cursor.fetchall()

        tk.Label(tab, text=f"Popular {item_type}s", font=("Arial", 24, "bold")).pack(pady=10)

        for row in items:
            item_id, name, desc, price, extra, nutri, avg_rating, num_reviews = row

            container = tk.Frame(tab, bd=1, relief="solid", padx=10, pady=5, cursor="hand2")
            container.pack(fill="x", padx=10, pady=5)

            #details frame
            details_frame = tk.Frame(container, bg="#f0f0f0", padx=10, pady=5)

            # Header with name + rating
            header = tk.Frame(container)
            header.pack(fill="x")
            tk.Label(header, text=name, font=("Arial",14,"bold")).pack(side="left")
            rating_disp = "No reviews yet." if num_reviews==0 else f"{round(avg_rating,1)}/5"
            tk.Label(header, text=f"Rating: {rating_disp}", font=("Arial",12)).pack(side="right")

            # toggle on click
            def toggle(df=details_frame):
                if df.winfo_ismapped(): df.pack_forget()
                else: df.pack(fill="x", padx=10, pady=5)
            # Bind both the container and header
            container.bind("<Button-1>", lambda e, df=details_frame: toggle(df))
            header.bind("<Button-1>",   lambda e, df=details_frame: toggle(df))

            # Populate the details_frame
            tk.Label(details_frame, text=f"Description: {desc}", anchor="w",
                     wraplength=600, justify="left").pack(fill="x", pady=2)
            tk.Label(details_frame, text=f"Expected Price: ${price}", anchor="w").pack(fill="x", pady=2)
            if item_type=="Recipe":
                tk.Label(details_frame, text=f"Cooking Instructions: {extra}", anchor="w",
                         wraplength=600, justify="left").pack(fill="x", pady=2)
            else:
                tk.Label(details_frame, text=f"Duration: {extra} days", anchor="w").pack(fill="x", pady=2)
            tk.Label(details_frame, text=f"Nutritional Info: {nutri}", anchor="w",
                     wraplength=600, justify="left").pack(fill="x", pady=2)

            # review and save buttons
            tk.Button(details_frame, text="Leave a Review",
                      command=lambda it=item_type, iid=item_id, nm=name:
                          self.open_review_dialog_prefilled(it, iid, nm)
            ).pack(anchor="e", pady=5)

            tk.Button(details_frame, text=f"Save {item_type}",
                      command=lambda it=item_type, iid=item_id:
                          self.save_item(it, iid)
            ).pack(anchor="e", pady=2)

    def display_my_reviews(self):
        cursor = self.connection.cursor()
        query = """
            SELECT R.RDescription, R.Rating, R.Review_Type, 
                IFNULL(M.MName, Re.RName) AS ItemName
            FROM ReviewRating AS R
            LEFT JOIN MealPlan AS M ON R.Item_ID = M.Meal_Plan_ID AND R.Review_Type='MealPlan'
            LEFT JOIN Recipe AS Re ON R.Item_ID = Re.Recipe_ID AND R.Review_Type='Recipe'
            WHERE R.Customer_ID = %s
        """
        cursor.execute(query, (self.customer_id,))
        reviews = cursor.fetchall()

        tk.Label(self.my_reviews_tab, text="My Reviews", font=("Arial", 24, "bold")).pack(pady=10)

        for text, rating, rtype, name in reviews:
            frame = tk.Frame(self.my_reviews_tab, bd=1, relief="solid", padx=10, pady=5)
            frame.pack(fill="x", padx=10, pady=5)
            tk.Label(frame, text=f"{rtype}: {name}", font=("Arial", 14)).pack(anchor="w")
            tk.Label(frame, text=f"Rating: {rating}/5", font=("Arial", 12)).pack(anchor="w")
            tk.Label(frame, text=text, font=("Arial", 10)).pack(anchor="w")

    def save_item(self, item_type, item_id):
        cursor = self.connection.cursor()
        if item_type == "Recipe":
            cursor.execute(
                "INSERT IGNORE INTO RSavedBy (Customer_ID, ID) VALUES (%s, %s)",
                (self.customer_id, item_id)
            )
        else:  # MealPlan
            cursor.execute(
                "INSERT IGNORE INTO MSavedBy (Customer_ID, ID) VALUES (%s, %s)",
                (self.customer_id, item_id)
            )
        self.connection.commit()
        messagebox.showinfo("Saved", f"{item_type} saved to your saved items.")
        # Refresh the Saved Items tab
        for w in self.saved_items_tab.winfo_children():
            w.destroy()
        self.display_my_saved_items()

    '''---------------------------------------
            Refreshes pages
    ---------------------------------------'''
    def refresh_my_reviews_tab(self):
        for widget in self.my_reviews_tab.winfo_children():
            widget.destroy()
        self.display_my_reviews()

    def refresh_my_friends_tab(self):
        for widget in self.friends_tab.winfo_children():
            widget.destroy()
        self.display_friends()

    def refresh_popular_items_tab(self, tab, item_type):
        for w in tab.winfo_children():
            w.destroy()
        self.display_popular_items(tab, item_type)




class DBAppAdmin:
    def __init__(self, root, connection, user):
        self.root = root
        self.conn = connection
        self.user_id = user['User_ID']

        # Header
        header = tk.Label(root, text="Admin Dashboard", bg="#003366", fg="white", font=("Arial", 24, "bold"))
        header.pack(fill="x", pady=(0,10))

        # Tabs
        tab_control = ttk.Notebook(root)
        tab_control.pack(expand=1, fill="both")

        self.user_tab = tk.Frame(tab_control)
        tab_control.add(self.user_tab, text="User Management")

        self.report_tab = tk.Frame(tab_control)
        tab_control.add(self.report_tab, text="Reports")

        # Populate tabs
        self._build_user_tab()
        self._build_report_tab()

    def _build_user_tab(self):
        # Treeview of existing users
        cols = ("Username","Role","Created_By","Created_At")
        self.tree = ttk.Treeview(self.user_tab, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Load users
        cursor = self.conn.cursor()
        cursor.execute("SELECT Username, Role, Created_By, Created_At FROM Users ORDER BY Created_At DESC")
        for u,r,cb,ca in cursor.fetchall():
            self.tree.insert("","end", values=(u,r,cb or '', ca))

        # Form to add new user
        form = ttk.LabelFrame(self.user_tab, text="Create New User")
        form.pack(fill="x", padx=10, pady=(0,10))
        tk.Label(form, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.new_username = tk.Entry(form)
        self.new_username.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(form, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.new_password = tk.Entry(form, show="*")
        self.new_password.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(form, text="Role:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.new_role = ttk.Combobox(form, values=["admin","employee","customer"], state="readonly")
        self.new_role.current(2)
        self.new_role.grid(row=2, column=1, padx=5, pady=5)

        btn = tk.Button(form, text="Create User", command=self._create_user)
        btn.grid(row=3, column=0, columnspan=2, pady=10)

    def _create_user(self):
        uname = self.new_username.get().strip()
        pw    = self.new_password.get()
        role  = self.new_role.get()
        if not uname or not pw or not role:
            messagebox.showwarning("Input Error","All fields are required.")
            return
        try:
            auth.create_user(uname, pw, role, created_by=self.user_id)
            messagebox.showinfo("Success", f"User '{uname}' created as {role}.")
            # Refresh treeview
            for row in self.tree.get_children():
                self.tree.delete(row)
            cursor = self.conn.cursor()
            cursor.execute("SELECT Username, Role, Created_By, Created_At FROM Users ORDER BY Created_At DESC")
            for u,r,cb,ca in cursor.fetchall():
                self.tree.insert("","end", values=(u,r,cb or '', ca))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _build_report_tab(self):
        # Simple stats
        stats_frame = tk.Frame(self.report_tab)
        stats_frame.pack(fill="x", padx=10, pady=10)
        cursor = self.conn.cursor()
        stats = []
        queries = [
            ("Total Customers", "SELECT COUNT(*) FROM Customers"),
            ("Total Recipes",   "SELECT COUNT(*) FROM Recipe"),
            ("Total Meal Plans","SELECT COUNT(*) FROM MealPlan"),
            ("Total Users",     "SELECT COUNT(*) FROM Users")
        ]
        for i, (label, q) in enumerate(queries):
            cursor.execute(q)
            count = cursor.fetchone()[0]
            tk.Label(stats_frame, text=f"{label}: {count}", font=("Arial",14)).grid(row=i, column=0, sticky="w", pady=2)

        
        # Tabbed interface
        tab_control = ttk.Notebook(stats_frame)
        tab_control.grid(row=len(queries), column=0, sticky="w", pady=2)

        # Tab 1: Recipe Data
        self.recipe_report_tab = tk.Frame(tab_control)
        tab_control.add(self.recipe_report_tab, text="Recipe Data")
        self.display_recipe_data()

        # Tab 2: Meal Plan Data
        self.meal_plan_report_tab = tk.Frame(tab_control)
        tab_control.add(self.meal_plan_report_tab, text="Meal Plan Data")
        self.display_meal_plan_data()

    def display_recipe_data(self):
        cursor = self.conn.cursor()
        query = "SELECT * FROM ReviewRating WHERE Review_Type = 'Recipe';"
        cursor.execute(query)
        reviews = cursor.fetchall()

        ratings = [row[4] for row in reviews]
        rating_counts = Counter(ratings)
        counts = [rating_counts.get(i, 0) for i in range(1, 6)]

        # Create graph
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.bar(range(1, 6), counts, color='skyblue', edgecolor='black')
        ax.set_title('Distribution of Review Ratings')
        ax.set_xlabel('Rating (Stars)')
        ax.set_ylabel('Number of Reviews')
        ax.set_xticks(range(1, 6))

        # place graph on GUI instead of new window
        canvas = FigureCanvasTkAgg(fig, master=self.recipe_report_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        recipe_ratings = {}
        for review in reviews:
            if review[2] == "Recipe":
                id  = review[3]
                if id in recipe_ratings:
                    recipe_ratings[id] += [review[4]]
                else:
                    recipe_ratings[id] = [review[4]]

        min_ratings_req = 2
        averages = {k: sum(v) / len(v) for k, v in recipe_ratings.items() if len(v) >= min_ratings_req}
        max_key = max(averages, key=averages.get) 
        #print(max_key)

        query = "SELECT RNAME FROM Recipe WHERE Recipe_ID = %s"
        cursor.execute(query, (max_key,))
        ba_review_recipe_name = cursor.fetchall()

        tk.Label(self.recipe_report_tab, text=f"{ba_review_recipe_name[0][0]} is the recipe with the best average rating, with an average of {averages[max_key]}.", font=("Arial", 10)).pack(fill="x", pady=2)

        query = "SELECT * FROM RSAVEDBY"
        cursor.execute(query)
        saved_info = cursor.fetchall()
        #print(saved_info)

        save_counts = {}
        for save_pair in saved_info:
            recipe_id = save_pair[1]
            if recipe_id in save_counts:
                save_counts[recipe_id] += 1
            else:
                save_counts[recipe_id] = 1
        max_key = max(save_counts, key=save_counts.get)
        #print(max_key)
        query = "SELECT RNAME FROM Recipe WHERE Recipe_ID = %s"
        cursor.execute(query, (max_key,))
        sa_review_recipe_name = cursor.fetchall()

        tk.Label(self.recipe_report_tab, text=f"{sa_review_recipe_name[0][0]} is the recipe with the most saves, with {save_counts[max_key]} saves.", font=("Arial", 10)).pack(fill="x", pady=2)

    def display_meal_plan_data(self):
        cursor = self.conn.cursor()
        query = "SELECT * FROM ReviewRating WHERE Review_Type = 'MealPlan';"
        cursor.execute(query)
        reviews = cursor.fetchall()

        ratings = [row[4] for row in reviews]
        rating_counts = Counter(ratings)
        counts = [rating_counts.get(i, 0) for i in range(1, 6)]

        # Create graph
        mp_fig, mp_ax = plt.subplots(figsize=(5, 4))
        mp_ax.bar(range(1, 6), counts, color='skyblue', edgecolor='black')
        mp_ax.set_title('Distribution of Review Ratings')
        mp_ax.set_xlabel('Rating (Stars)')
        mp_ax.set_ylabel('Number of Reviews')
        mp_ax.set_xticks(range(1, 6))

        # place graph on GUI instead of new window
        canvas = FigureCanvasTkAgg(mp_fig, master=self.meal_plan_report_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        recipe_ratings = {}
        for review in reviews:
            if review[2] == "MealPlan":
                id  = review[3]
                if id in recipe_ratings:
                    recipe_ratings[id] += [review[4]]
                else:
                    recipe_ratings[id] = [review[4]]

        min_ratings_req = 2
        averages = {k: sum(v) / len(v) for k, v in recipe_ratings.items() if len(v) >= min_ratings_req}
        max_key = max(averages, key=averages.get) 
        #print(max_key)

        query = "SELECT MNAME FROM MealPlan WHERE Meal_Plan_ID = %s"
        cursor.execute(query, (max_key,))
        ba_review_recipe_name = cursor.fetchall()

        tk.Label(self.meal_plan_report_tab, text=f"{ba_review_recipe_name[0][0]} is the meal plan with the best average rating, with an average of {averages[max_key]}.", font=("Arial", 10)).pack(fill="x", pady=2)

        query = "SELECT * FROM MSAVEDBY"
        cursor.execute(query)
        saved_info = cursor.fetchall()
        #print(saved_info)

        save_counts = {}
        for save_pair in saved_info:
            recipe_id = save_pair[1]
            if recipe_id in save_counts:
                save_counts[recipe_id] += 1
            else:
                save_counts[recipe_id] = 1
        max_key = max(save_counts, key=save_counts.get)
        #print(max_key)
        query = "SELECT MNAME FROM MealPlan WHERE Meal_Plan_ID = %s"
        cursor.execute(query, (max_key,))
        sa_review_recipe_name = cursor.fetchall()

        tk.Label(self.meal_plan_report_tab, text=f"{sa_review_recipe_name[0][0]} is the meal plan with the most saves, with {save_counts[max_key]} saves.", font=("Arial", 10)).pack(fill="x", pady=2)

