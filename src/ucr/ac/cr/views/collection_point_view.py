# views/collection_point_view.py
import tkinter as tk
from tkinter import ttk

class CollectionPointView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        tk.Label(self, text="Gestión de Puntos de Recolección").pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("id", "nombre", "ubicación", "distrito", "capacidad", "carga", "activo"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("ubicación", text="Ubicación")
        self.tree.heading("distrito", text="Distrito")
        self.tree.heading("capacidad", text="Capacidad (kg)")
        self.tree.heading("carga", text="Carga actual (kg)")
        self.tree.heading("activo", text="Activo")
        self.tree.pack(fill="both", expand=True)

        tk.Button(self, text="Cargar puntos",
                  command=self.load_points).pack(pady=5)

    def load_points(self):
        self.tree.delete(*self.tree.get_children())
        for p in self.controller.get_all_points():
            self.tree.insert("", "end", values=(
                p["point_id"], p["name"], p["location"], p["district"],
                p["capacity_kg"], p["current_load_kg"], p["is_active"]
            ))
