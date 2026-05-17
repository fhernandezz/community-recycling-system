import tkinter as tk
from tkinter import ttk

from .recycler_view import RecyclerView
from .collection_point_view import CollectionPointView
from .record_view import RecordView

class MainApp(tk.Tk):
    def __init__(self, recycler_controller, point_controller, record_controller):
        super().__init__()
        self.title("Sistema de Reciclaje Comunitario")
        self.geometry("900x600")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        notebook.add(RecyclerView(notebook, recycler_controller), text="Recicladores")
        notebook.add(CollectionPointView(notebook, point_controller), text="Puntos")
        notebook.add(RecordView(notebook, record_controller), text="Registros")
