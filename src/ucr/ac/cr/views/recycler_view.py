import tkinter as tk
from tkinter import ttk

class RecyclerView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        tk.Label(self, text="Gestión de Recicladores").pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("id", "nombre", "cédula", "email", "teléfono", "distrito"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("cédula", text="Cédula")
        self.tree.heading("email", text="Email")
        self.tree.heading("teléfono", text="Teléfono")
        self.tree.heading("distrito", text="Distrito")
        self.tree.pack(fill="both", expand=True)

        tk.Button(self, text="Cargar recicladores",
                  command=self.load_recyclers).pack(pady=5)

    def load_recyclers(self):
        self.tree.delete(*self.tree.get_children())
        for r in self.controller.get_all_recyclers():
            self.tree.insert("", "end", values=(
                r["recycler_id"], r["full_name"], r["id_number"],
                r["email"], r["phone"], r["district"]
            ))