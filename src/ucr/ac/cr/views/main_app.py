import tkinter as tk
from tkinter import ttk

from src.ucr.ac.cr.views.recycler_view import RecyclerView
from src.ucr.ac.cr.views.collection_point_view import CollectionPointView
from src.ucr.ac.cr.views.record_view import RecordView
from src.ucr.ac.cr.views.reports_view import ReportsView

class MainApp(tk.Tk):
    def __init__(self, recycler_controller, point_controller, record_controller):
        super().__init__()
        self.title("Sistema de Reciclaje Comunitario")
        self.geometry("1000x650")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        notebook.add(
            RecyclerView(notebook, recycler_controller),
            text="Recicladores"
        )
        notebook.add(
            CollectionPointView(notebook, point_controller),
            text="Puntos de Recolección"
        )
        notebook.add(
            RecordView(notebook, recycler_controller, point_controller, record_controller),
            text="Entregas"
        )
        notebook.add(
            ReportsView(notebook, record_controller),
            text="Reportes"
        )