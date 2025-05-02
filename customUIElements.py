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
    def __init__(self, master, item_name, *args, font_size = 14, can_edit = True, use_args_order = True, **kwargs):
        super().__init__(master, **kwargs)
        self.expanded = False
        self.detail_frame = None
        self.attributes = args
        self.can_edit = can_edit
        self.use_args_order = use_args_order

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

            args_order = ["Description", "Price", "Cooking Instructions", "Nutritional Information"]
            for i, arg in enumerate(self.attributes):
                if i < len(args_order):
                    s = ""
                    if self.use_args_order:
                        s += args_order[i] + ":"

                    tk.Label(self.detail_frame, text=f"{s} {arg}", anchor="w").pack(fill="x")
                else:
                    w = ExpandableItem(self.detail_frame, arg[0], *(arg[1:]), font_size=10, use_args_order=False)
                    w.pack(fill="x")
            #tk.Label(self.detail_frame, text=f"Price: ${self.price}", anchor="w").pack(fill="x")

            if self.can_edit:
                tk.Button(self.detail_frame, text="Edit", command=self.edit_item).pack(anchor="e", pady=5)
            self.detail_frame.pack(fill="x")
            self.expanded = True

    def edit_item(self):
        print("Need to implement editing logic")
