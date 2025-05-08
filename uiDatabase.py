import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk

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

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.label.config(text="Disconnected", fg="red")

    '''--------------------------------------------------
    
        FUNCTIONS THAT POPULATE MAJOR TAB PAGES

    --------------------------------------------------'''
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

                l = tk.Label(new_window, text="Ingredient ID: ", anchor="w").grid(row=0, column=0, padx=10, pady=5)
                e = tk.Entry(new_window)
                e.grid(row=0, column=1, padx=10, pady=5)

                def submit_add():
                    entries = [child for child in new_window.winfo_children() if isinstance(child, tk.Entry)]
                    results = [entry.get() for entry in entries]
                    ingredient_id = results[0]
                    #print(results)

                    cursor = self.connection.cursor()
                    query = """
                        INSERT IGNORE INTO GroceryListItems (List_ID, Ingredient_ID)
                        VALUES (%s, %s)
                        """
                    cursor.execute(query, (list_id,ingredient_id,))
                    self.connection.commit()

                    if cursor.rowcount > 0:
                        messagebox.showinfo("Success", "Grocery List updated successfully.")

                        query = """
                            SELECT * 
                            FROM Ingredient
                            WHERE Ingredient_ID = %s;
                            """
                        cursor.execute(query, (ingredient_id,))
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
                        messagebox.showinfo("No Change", "No customer was updated.") 
                    

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
            r_query = "SELECT * FROM Recipe AS R WHERE R.Created_By = " + str(self.customer_id) #WHERE R.Recipe_ID <= 10"
            mp_query = "SELECT * FROM MealPlan AS MP WHERE MP.Created_By = " + str(self.customer_id) #WHERE MP.Meal_Plan_ID <= 10"
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
            tk.Label(self.saved_items_tab, text="My Created Items", font=("Arial", 32, "bold")).grid(row=0, column=0, padx=(0,25), pady=5, sticky="w")
            
            tk.Button(self.saved_items_tab, text="Add Item  +", width=20, command=self.add_item).grid(row=0, column=1, padx=(0,25), pady=5, sticky="e")


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
            
            '''
            My Friends UI
            '''
            # Header
            tk.Label(self.friends_tab, text="My Friends", font=("Arial", 32, "bold")).grid(row=0, column=0, padx=(0,25), pady=5, sticky="w")
            
            #tk.Button(self.my_items_tab, text="Add Item  +", width=20, command=self.add_item).grid(row=0, column=1, padx=(0,25), pady=5, sticky="e")

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
        
        
    '''
    Function to add an item to list
    TODO NEED TO IMPLEMENT, should probably make this sub function like grocery list's add
    '''
    def add_item(self):
        #TODO: implement
        print("need to implement")

