import tkinter as tk
from tkinter import messagebox


class LoginView(tk.Tk):

    def __init__(self, recycler_controller, on_login_success):
        super().__init__()
        self.title("Sistema de Reciclaje — Iniciar sesión")
        self.geometry("360x230")
        self.resizable(False, False)

        self._recycler_controller = recycler_controller
        self._on_login_success = on_login_success

        tk.Label(self, text="Sistema de Reciclaje Comunitario",
                 font=("Arial", 13, "bold")).pack(pady=(25, 10))

        form_frame = tk.Frame(self)
        form_frame.pack(pady=5)

        tk.Label(form_frame, text="ID Usuario:", width=14, anchor="e").grid(
            row=0, column=0, padx=5, pady=6)
        self._id_entry = tk.Entry(form_frame, width=22)
        self._id_entry.grid(row=0, column=1, padx=5, pady=6)

        tk.Label(form_frame, text="Contraseña:", width=14, anchor="e").grid(
            row=1, column=0, padx=5, pady=6)
        self._password_entry = tk.Entry(form_frame, width=22, show="*")
        self._password_entry.grid(row=1, column=1, padx=5, pady=6)

        tk.Button(self, text="Ingresar", width=16,
                  command=self._handle_login).pack(pady=12)

        self.bind("<Return>", lambda event: self._handle_login())

    def _handle_login(self):
        recycler_id = self._id_entry.get().strip()
        password = self._password_entry.get().strip()

        if not recycler_id or not password:
            messagebox.showwarning("Campos vacíos", "Ingresá tu ID y contraseña.")
            return

        if self._recycler_controller.validate_credentials(recycler_id, password):
            self.destroy()
            self._on_login_success()
        else:
            messagebox.showerror("Acceso denegado", "ID o contraseña incorrectos.")
            self._password_entry.delete(0, tk.END)