
import tkinter as tk
from tkinter import ttk

class RecordView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        tk.Label(self, text="Registros de Reciclaje").pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("id", "reciclador", "punto", "material", "peso", "fecha", "notas"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("reciclador", text="Reciclador")
        self.tree.heading("punto", text="Punto")
        self.tree.heading("material", text="Material")
        self.tree.heading("peso", text="Peso (kg)")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("notas", text="Notas")
        self.tree.pack(fill="both", expand=True)

        tk.Button(self, text="Cargar registros",
                  command=self.load_records).pack(pady=5)

    def load_records(self):
        self.tree.delete(*self.tree.get_children())
        for r in self.controller.get_records_by_date_range("2026-01-01", "2026-12-31"):
            self.tree.insert("", "end", values=(
                r["record_id"], r["recycler_id"], r["point_id"],
                r["material_type"], r["weight_kg"], r["record_date"], r["notes"]
            ))
