import tkinter as tk
from tkinter import ttk, messagebox


class RecordView(tk.Frame):

    def __init__(self, master, recycler_controller, point_controller, record_controller):
        super().__init__(master)
        self._recycler_controller = recycler_controller
        self._point_controller = point_controller
        self._record_controller = record_controller
        self._build_form()
        self._build_table()
        self.load_records()

    def _build_form(self):
        tk.Label(self, text="Registrar Entrega de Material",
                 font=("Arial", 12, "bold")).pack(pady=(10, 5))

        form_frame = tk.Frame(self)
        form_frame.pack()

        # ID Registro
        tk.Label(form_frame, text="ID Registro:", width=20, anchor="e").grid(
            row=0, column=0, padx=5, pady=3)
        self._record_id_entry = tk.Entry(form_frame, width=30)
        self._record_id_entry.grid(row=0, column=1, padx=5, pady=3)

        # Reciclador — combobox
        tk.Label(form_frame, text="Reciclador:", width=20, anchor="e").grid(
            row=1, column=0, padx=5, pady=3)
        self._recycler_var = tk.StringVar()
        self._recycler_combo = ttk.Combobox(form_frame, textvariable=self._recycler_var,
                                            width=28, state="readonly")
        self._recycler_combo.grid(row=1, column=1, padx=5, pady=3)

        # Punto de recolección — combobox
        tk.Label(form_frame, text="Punto de recolección:", width=20, anchor="e").grid(
            row=2, column=0, padx=5, pady=3)
        self._point_var = tk.StringVar()
        self._point_combo = ttk.Combobox(form_frame, textvariable=self._point_var,
                                         width=28, state="readonly")
        self._point_combo.grid(row=2, column=1, padx=5, pady=3)

        # Material — combobox
        tk.Label(form_frame, text="Material:", width=20, anchor="e").grid(
            row=3, column=0, padx=5, pady=3)
        self._material_var = tk.StringVar()
        self._material_combo = ttk.Combobox(
            form_frame, textvariable=self._material_var, width=28, state="readonly",
            values=["plástico", "vidrio", "papel", "metal", "orgánico"]
        )
        self._material_combo.grid(row=3, column=1, padx=5, pady=3)

        # Peso
        tk.Label(form_frame, text="Peso (kg):", width=20, anchor="e").grid(
            row=4, column=0, padx=5, pady=3)
        self._weight_entry = tk.Entry(form_frame, width=30)
        self._weight_entry.grid(row=4, column=1, padx=5, pady=3)

        # Notas
        tk.Label(form_frame, text="Notas (opcional):", width=20, anchor="e").grid(
            row=5, column=0, padx=5, pady=3)
        self._notes_entry = tk.Entry(form_frame, width=30)
        self._notes_entry.grid(row=5, column=1, padx=5, pady=3)

        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=5)
        tk.Button(buttons_frame, text="Registrar Entrega",
                  command=self._handle_register).pack(side="left", padx=5)
        tk.Button(buttons_frame, text="Recargar listas",
                  command=self._reload_combos).pack(side="left", padx=5)

        self._reload_combos()

    def _build_table(self):
        tk.Label(self, text="Entregas registradas",
                 font=("Arial", 11, "bold")).pack(pady=(10, 2))

        columns = ("id", "reciclador", "punto", "material", "peso", "fecha", "notas")
        self._table = ttk.Treeview(self, columns=columns, show="headings", height=8)

        headers = {
            "id": "ID", "reciclador": "Reciclador", "punto": "Punto",
            "material": "Material", "peso": "Peso (kg)",
            "fecha": "Fecha", "notas": "Notas"
        }
        for col_key, col_label in headers.items():
            self._table.heading(col_key, text=col_label)
            self._table.column(col_key, width=110)

        self._table.pack(fill="both", expand=True, padx=10)
        tk.Button(self, text="Actualizar lista", command=self.load_records).pack(pady=5)

    def _reload_combos(self):
        recyclers = self._recycler_controller.get_all_recyclers()
        self._recycler_map = {
            f"{recycler.recycler_id} — {recycler.full_name}": recycler.recycler_id
            for recycler in recyclers
        }
        self._recycler_combo["values"] = list(self._recycler_map.keys())

        points = self._point_controller.get_all_points()
        self._point_map = {
            f"{point.point_id} — {point.name}": point.point_id
            for point in points
        }
        self._point_combo["values"] = list(self._point_map.keys())

    def _handle_register(self):
        recycler_key  = self._recycler_var.get()
        point_key     = self._point_var.get()
        material_type = self._material_var.get()

        if not recycler_key or not point_key or not material_type:
            messagebox.showwarning("Campos vacíos",
                                   "Seleccioná un reciclador, punto de recolección y material.")
            return

        try:
            weight_kg = float(self._weight_entry.get())
        except ValueError:
            messagebox.showerror("Error", "El peso debe ser un número válido.")
            return

        try:
            self._record_controller.register_delivery(
                record_id=self._record_id_entry.get(),
                recycler_id=self._recycler_map[recycler_key],
                point_id=self._point_map[point_key],
                material_type=material_type,
                weight_kg=weight_kg,
                notes=self._notes_entry.get()
            )
            messagebox.showinfo("Éxito", "Entrega registrada correctamente.")
            self._record_id_entry.delete(0, tk.END)
            self._recycler_var.set("")
            self._point_var.set("")
            self._material_var.set("")
            self._weight_entry.delete(0, tk.END)
            self._notes_entry.delete(0, tk.END)
            self.load_records()
        except ValueError as validation_error:
            messagebox.showerror("Error de validación", str(validation_error))
        except Exception as unexpected_error:
            messagebox.showerror("Error inesperado", str(unexpected_error))

    def load_records(self):
        self._table.delete(*self._table.get_children())
        for record in self._record_controller.get_all_records():
            self._table.insert("", "end", values=(
                record.record_id,
                record.recycler_id,
                record.point_id,
                record.material_type,
                record.weight_kg,
                record.record_date,
                record.notes
            ))