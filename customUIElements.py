import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk
from enum import Enum

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
    def __init__(self, master, connection, item_name, item_type, *args, font_size = 14, can_edit = True, use_args_order = True, is_sub_item = False, customer_id = 1, **kwargs):
        super().__init__(master, **kwargs)
        self.expanded = False
        self.detail_frame = None
        self.attributes = args
        self.can_edit = can_edit
        self.use_args_order = use_args_order
        self.is_sub_item = is_sub_item
        self.item_type = item_type
        self.item_name = item_name
        self.connection = connection
        self.args_order = ["Description", "Expected Price", "Cooking Instructions", "Nutritional Info"] if self.item_type == ItemType.RECIPE else ["Description", "Expected Price", "Duration", "Nutritional Info"]
        self.customer_id = customer_id

        #print(self.attributes)
        font_style = ("Arial", font_size)
        if self.is_sub_item:
            font_style = ("Arial", font_size, "bold")

        self.button = tk.Button(self, 
            text=item_name, 
            font=font_style, 
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

            '''
            Placing all the elements in the expanded portion
            '''
            for i, arg in enumerate(self.attributes):

                if i < len(self.args_order):
                    s = ""
                    if self.use_args_order:
                       s += self.args_order[i] + ":"

                    if not self.is_sub_item:
                        tk.Label(self.detail_frame, text=f"{s} {arg}", anchor="w").pack(fill="x")
                    else:
                        cursor = self.connection.cursor()
            
                        if self.item_type == ItemType.RECIPE:
                            r_query = "SELECT * FROM Recipe AS R WHERE R.RName = %s"
                            cursor.execute(r_query, (arg,))
                            r_result = cursor.fetchall()[0]

                            ri_query = """
                                SELECT I.* 
                                FROM RecipeIngredient AS RI 
                                JOIN Ingredient AS I ON RI.Ingredient_ID = I.Ingredient_ID
                                JOIN RECIPE AS R ON RI.Recipe_ID = R.Recipe_ID
                                WHERE R.RName = %s"""
                            cursor.execute(ri_query, (arg,))
                            ri_result = cursor.fetchall()
                            #print("searchring for id:", row[0], "ri result:", ri_result)

                            s = ["Ingredients"] + [row[1] for row in ri_result]
                            #print(r_result)
                            #print(s)
                            
                            w = ExpandableItem(self.detail_frame, self.connection, arg, self.item_type, r_result[3], r_result[5], r_result[2], r_result[4], s, font_size=10, can_edit=False).pack(fill="x")
                        elif self.item_type == ItemType.CUSTOMER:
                            r_query = "SELECT * FROM Recipe AS R WHERE R.Created_By = %s"
                            cursor.execute(r_query, (arg,))
                            r_results = cursor.fetchall()

                            m_query = "SELECT * FROM MealPlan AS M WHERE M.Created_By = %s"
                            cursor.execute(m_query, (arg,))
                            m_results = cursor.fetchall()

                            #print("recipes:", r_results)
                            #print("meal pleans:", m_results)
                            if len(r_results) > 0:
                                tk.Label(self.detail_frame, text="Recipes:", font=("Arial", 10, "bold"), anchor="w").pack(fill="x")
                            for r_result in r_results:
                                ri_query = """
                                    SELECT I.* 
                                    FROM RecipeIngredient AS RI 
                                    JOIN Ingredient AS I ON RI.Ingredient_ID = I.Ingredient_ID
                                    JOIN RECIPE AS R ON RI.Recipe_ID = R.Recipe_ID
                                    WHERE R.RName = %s"""
                                cursor.execute(ri_query, (r_result[1],))
                                ri_result = cursor.fetchall()
                                #print("searchring for id:", row[0], "ri result:", ri_result)

                                s = ["Ingredients"] + [row[1] for row in ri_result]

                                ingredients_frame = tk.Frame(self.detail_frame)
                                ingredients_frame.pack(fill="x")

                                ExpandableItem(ingredients_frame, self.connection, r_result[1], ItemType.RECIPE, r_result[3], r_result[5], r_result[2], r_result[4], s, font_size=10, can_edit=False).pack(side="left", fill="x", expand=True)
                                tk.Button(ingredients_frame, text="Save Recipe", command=lambda r_id=r_result[0]: self.save_recipe(r_id)).pack(side="right")
                                #w = ExpandableItem(self.detail_frame, self.connection, r_result[1], ItemType.RECIPE, r_result[3], r_result[5], r_result[2], r_result[4], s, font_size=10, can_edit=False).pack(fill="x")

                            if len(m_results) > 0:
                                tk.Label(self.detail_frame, text="Meal Plans:", font=("Arial", 10, "bold"), anchor="w").pack(fill="x")
                            for row in m_results:
                                mr_query = """
                                    SELECT R.* 
                                    FROM MealPlanRecipe AS MR 
                                    JOIN Recipe AS R ON MR.Recipe_ID = R.Recipe_ID
                                    WHERE MR.MealPlan_ID = %s"""
                                cursor.execute(mr_query, (row[0],))
                                mr_result = cursor.fetchall()
                                
                                s = ["Recipes"] + [row[1] for row in mr_result]
                                #print(s)

                                recipe_frame = tk.Frame(self.detail_frame)
                                recipe_frame.pack(fill="x")

                                ExpandableItem(recipe_frame, self.connection, row[1], ItemType.MEALPLAN, row[4], row[3], row[2], row[5], s, font_size=10, can_edit=False).pack(side="left", fill="x", expand=True)
                                tk.Button(recipe_frame, text="Save Meal Plan", command=lambda m_id=row[0]: self.save_meal_plan(m_id)).pack(side="right")
                        
                        else: 
                            ExpandableItem(self.detail_frame, self.connection, arg, self.item_type, "add details here", font_size=10, can_edit=False).pack(fill="x")
                else:
                    w = ExpandableItem(self.detail_frame, self.connection, arg[0], self.item_type - 1, *(arg[1:]), font_size=10, use_args_order=False, is_sub_item=True, can_edit=self.can_edit)
                    w.pack(fill="x")
            
            '''
            Edit/Add/Remove button placement
            '''
            if self.can_edit:
                if not self.is_sub_item:
                    tk.Button(self.detail_frame, text="Edit", command=self.edit_item).pack(anchor="e", pady=5)
                else:
                    tk.Button(self.detail_frame, text=f"Remove {self.item_type}", command=self.remove_item).pack(anchor="e", pady=5)
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

            edit_query = f"UPDATE {self.item_type} AS {self.item_type[0]} SET "
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
                messagebox.showinfo("Success", (self.item_type + " updated successfully."))
                #for entry in self.update_entries.values():
                #    entry.delete(0, tk.END)

                # Step 1: Refresh self.attributes from the DB
                refreshed_query = f"SELECT * FROM {self.item_type} WHERE {self.item_type[0]}NAME = %s;"
                cursor.execute(refreshed_query, (self.item_name,))
                row = cursor.fetchone()
                if row:
                    if self.item_type == ItemType.RECIPE:
                        self.attributes = (row[3], row[5], row[2], row[4], self.attributes[4])  
                    elif self.item_type == ItemType.MEALPLAN:
                        #print(row)
                        #print(self.attributes)
                        self.attributes = (row[4], row[3], row[2], row[5])
                        #print(self.attributes)
                        
                    
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

    def remove_item(self):
        new_window = tk.Toplevel(self.master)
        new_window.title("Remove item")
        #l = tk.Label(new_window, text="Need to implement the ability to add/remove items", anchor="w").grid(row=0, column=0, padx=10, pady=5)

        entries = [child for child in self.detail_frame.winfo_children() if isinstance(child, ExpandableItem)]
        remove_entry_type = entries[0].item_type
        remove_names = [entry.item_name for entry in entries]
        #print(remove_entry_type, ", ", remove_names)


        self.checkbox_vars = []
        for i, arg in enumerate(remove_names):
            l = tk.Label(new_window, text=f"{arg}", anchor="w").grid(row=i, column=0, padx=10, pady=5)

            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(new_window, variable=var)
            checkbox.grid(row=i, column=1)
            self.checkbox_vars.append(var)

        def submit_remove():
            if isinstance(self.master.master, ExpandableItem):
                master_item = self.master.master
                
                results = [var.get() for var in self.checkbox_vars]
                #print(results)

                cursor = self.connection.cursor()
                e_query = """
                    SELECT * 
                    FROM """ + str(master_item.item_type) + """
                    WHERE """ + master_item.item_type[0] + """Name = %s
                    """
                    
                cursor.execute(e_query, (master_item.item_name,))
                e_result = cursor.fetchall()
                e_id = e_result[0][0]
                #print(e_id)

                for i, result in enumerate(results):
                    if result:
                        deleted_item_name = ""
                        for widget in new_window.grid_slaves(row=i):
                            if isinstance(widget, tk.Label):
                                if widget.grid_info()["column"] == 0:
                                    deleted_item_name = widget.cget('text')
                            widget.destroy()
                        
                        #print("item to delete is:", deleted_item_name)
                
                        #print(master_item.item_name, ", ", master_item.item_type)


                        re_query = """
                            SELECT * 
                            FROM """ + str(remove_entry_type) + """
                            WHERE """ + remove_entry_type[0] + """Name = %s
                            """
                            
                        cursor.execute(re_query, (deleted_item_name,))
                        re_result = cursor.fetchall()
                        re_id = re_result[0][0]
                        #print(re_id, ", ", e_id)
                        #print(str(master_item.item_type) + str(remove_entry_type))

                        r_query = """
                            DELETE FROM """ + str(master_item.item_type) + str(remove_entry_type) + """ WHERE """ + str(master_item.item_type) + """_ID = %s AND """ + str(remove_entry_type) + """_ID = %s;
                        """
                        cursor.execute(r_query, (e_id, re_id,))
                        self.connection.commit()
                        #re_id = re_result[0][0]

                        if cursor.rowcount > 0:
                            messagebox.showinfo("Success", "Items deleted successfully.")
                        else:
                            messagebox.showinfo("No Change", "No item deleted.") 

        tk.Button(new_window, text="Remove Selected Items", width=20, command=submit_remove).grid(row=4, column=0, columnspan=2, padx=(0,25), pady=5, sticky="ew")

        #TODO: send message to main ui to update accordingly

    def save_recipe(self, recipe_id):
        #print(f"Customer {self.customer_id} wants to save {recipe_id}")
        
        cursor = self.connection.cursor()
        query = """
            INSERT IGNORE INTO RSavedBy (Customer_ID, ID)
            VALUES (%s, %s)
            """
        cursor.execute(query, (self.customer_id,recipe_id,))
        self.connection.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Success", "Your Saved Items updated successfully.")
        else:
            messagebox.showinfo("No Change", "No Item was saved.") 

    def save_meal_plan(self, meal_plan_id):
        #print(f"Customer {self.customer_id} wants to save {meal_plan_id}")

        cursor = self.connection.cursor()
        query = """
            INSERT IGNORE INTO MSavedBy (Customer_ID, ID)
            VALUES (%s, %s)
            """
        cursor.execute(query, (self.customer_id,meal_plan_id,))
        self.connection.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Success", "Your Saved Items updated successfully.")
        else:
            messagebox.showinfo("No Change", "No Item was saved.") 


class ItemType(Enum):
    CUSTOMER = 3
    MEALPLAN = 2
    RECIPE = 1
    INGREDIENT = 0

    #allows for addition with item_type
    #returns self + value, ex ingredient + 1 = recipe
    def __add__(self, value):
        if isinstance(value, int):
            sum = self.value + value

            for possible_type in ItemType:
                if possible_type.value == sum:
                    return possible_type
                
            raise ValueError("No possible enum value for {sum}")
        
        if isinstance(value, str):
            new_str = self.name + value

            return new_str
        raise TypeError("Cannot add {value.__class__} with ItemType. Must be int or string.")

    #allows for subtraction with item_type
    #returns self - value, ex meal_plan - 1 = recipe
    def __sub__(self, value):
        if isinstance(value, int):
            diff = self.value - value

            for possible_type in ItemType:
                if possible_type.value == diff:
                    return possible_type
                
            raise ValueError("No possible enum value for {diff}")
        raise TypeError("Can only subtract an integer from ItemType")
    
    def __str__(self):
        return {
            ItemType.RECIPE: "Recipe",
            ItemType.MEALPLAN: "MealPlan",
            ItemType.CUSTOMER: "Customers",
            ItemType.INGREDIENT: "Ingredient"
        }[self]
    
    def __getitem__(self, index):
        return self.name[index]
    
    