import tkinter as tk
from tkinter import ttk, messagebox

class RecyclerView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self._controller = controller
        self._build_form()
        self._build_table()
        self.load_recyclers()

    def _build_form(self):
        tk.Label(self, text="Registrar Reciclador",
                 font=("Arial", 12, "bold")).pack(pady=(10, 5))

        form_frame = tk.Frame(self)
        form_frame.pack()

        fields = [
            ("ID Reciclador:", "recycler_id"),
            ("Nombre completo:", "full_name"),
            ("Cédula:", "id_number"),
            ("Correo:", "email"),
            ("Teléfono:", "phone"),
            ("Distrito:", "district"),
        ]

        self._entries = {}
        for row_index, (label_text, field_key) in enumerate(fields):
            tk.Label(form_frame, text=label_text, width=18, anchor="e").grid(
                row=row_index, column=0, padx=5, pady=3)
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=row_index, column=1, padx=5, pady=3)
            self._entries[field_key] = entry

        tk.Button(self, text="Registrar", command=self._handle_register).pack(pady=6)

    def _build_table(self):
        tk.Label(self, text="Recicladores registrados",
                 font=("Arial", 11, "bold")).pack(pady=(10, 2))

        columns = ("id", "nombre", "cédula", "email", "teléfono", "distrito", "activo")
        self._table = ttk.Treeview(self, columns=columns, show="headings", height=8)

        headers = {
            "id": "ID", "nombre": "Nombre", "cédula": "Cédula",
            "email": "Email", "teléfono": "Teléfono",
            "distrito": "Distrito", "activo": "Activo"
        }
        for col_key, col_label in headers.items():
            self._table.heading(col_key, text=col_label)
            self._table.column(col_key, width=110)

        self._table.pack(fill="both", expand=True, padx=10)
        tk.Button(self, text="Actualizar lista", command=self.load_recyclers).pack(pady=5)

    def _handle_register(self):
        try:
            self._controller.register_recycler(
                recycler_id=self._entries["recycler_id"].get(),
                full_name=self._entries["full_name"].get(),
                id_number=self._entries["id_number"].get(),
                email=self._entries["email"].get(),
                phone=self._entries["phone"].get(),
                district=self._entries["district"].get()
            )
            messagebox.showinfo("Éxito", "Reciclador registrado correctamente.")
            for entry in self._entries.values():
                entry.delete(0, tk.END)
            self.load_recyclers()
        except ValueError as validation_error:
            messagebox.showerror("Error de validación", str(validation_error))
        except Exception as unexpected_error:
            messagebox.showerror("Error inesperado", str(unexpected_error))

    def load_recyclers(self):
        self._table.delete(*self._table.get_children())
        for recycler in self._controller.get_all_recyclers():
            self._table.insert("", "end", values=(
                recycler.recycler_id,
                recycler.full_name,
                recycler.id_number,
                recycler.email,
                recycler.phone,
                recycler.district,
                "Sí" if recycler.is_active else "No"
            ))