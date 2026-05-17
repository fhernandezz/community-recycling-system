import tkinter as tk
from tkinter import ttk, messagebox

class CollectionPointView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self._controller = controller
        self._build_form()
        self._build_table()
        self.load_points()

    def _build_form(self):
        tk.Label(self, text="Registrar Punto de Recolección",
                 font=("Arial", 12, "bold")).pack(pady=(10, 5))

        form_frame = tk.Frame(self)
        form_frame.pack()

        fields = [
            ("ID Punto:", "point_id"),
            ("Nombre:", "name"),
            ("Ubicación:", "location"),
            ("Distrito:", "district"),
            ("Capacidad (kg):", "capacity_kg"),
        ]

        self._entries = {}
        for row_index, (label_text, field_key) in enumerate(fields):
            tk.Label(form_frame, text=label_text, width=18, anchor="e").grid(
                row=row_index, column=0, padx=5, pady=3)
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=row_index, column=1, padx=5, pady=3)
            self._entries[field_key] = entry

        tk.Label(form_frame, text="Materiales aceptados:", width=18, anchor="e").grid(
            row=len(fields), column=0, padx=5, pady=3)
        materials_frame = tk.Frame(form_frame)
        materials_frame.grid(row=len(fields), column=1, sticky="w")

        self._material_vars = {}
        for material_name in ["plástico", "vidrio", "papel", "metal", "orgánico"]:
            var = tk.BooleanVar()
            tk.Checkbutton(materials_frame, text=material_name, variable=var).pack(
                side="left", padx=3)
            self._material_vars[material_name] = var

        tk.Button(self, text="Registrar Punto", command=self._handle_register).pack(pady=6)

    def _build_table(self):
        tk.Label(self, text="Puntos de recolección registrados",
                 font=("Arial", 11, "bold")).pack(pady=(10, 2))

        columns = ("id", "nombre", "ubicación", "distrito", "capacidad", "carga", "activo")
        self._table = ttk.Treeview(self, columns=columns, show="headings", height=8)

        headers = {
            "id": "ID", "nombre": "Nombre", "ubicación": "Ubicación",
            "distrito": "Distrito", "capacidad": "Capacidad (kg)",
            "carga": "Carga actual (kg)", "activo": "Activo"
        }
        for col_key, col_label in headers.items():
            self._table.heading(col_key, text=col_label)
            self._table.column(col_key, width=110)

        self._table.pack(fill="both", expand=True, padx=10)
        tk.Button(self, text="Actualizar lista", command=self.load_points).pack(pady=5)

    def _handle_register(self):
        selected_materials = [
            material_name for material_name, var in self._material_vars.items()
            if var.get()
        ]
        try:
            capacity_kg = float(self._entries["capacity_kg"].get())
        except ValueError:
            messagebox.showerror("Error", "La capacidad debe ser un número válido.")
            return

        try:
            self._controller.register_collection_point(
                point_id=self._entries["point_id"].get(),
                name=self._entries["name"].get(),
                location=self._entries["location"].get(),
                district=self._entries["district"].get(),
                accepted_materials=selected_materials,
                capacity_kg=capacity_kg
            )
            messagebox.showinfo("Éxito", "Punto de recolección registrado correctamente.")
            for entry in self._entries.values():
                entry.delete(0, tk.END)
            for var in self._material_vars.values():
                var.set(False)
            self.load_points()
        except ValueError as validation_error:
            messagebox.showerror("Error de validación", str(validation_error))
        except Exception as unexpected_error:
            messagebox.showerror("Error inesperado", str(unexpected_error))

    def load_points(self):
        self._table.delete(*self._table.get_children())
        for point in self._controller.get_all_points():
            self._table.insert("", "end", values=(
                point.point_id,
                point.name,
                point.location,
                point.district,
                point.capacity_kg,
                point.current_load_kg,
                "Sí" if point.is_active else "No"
            ))