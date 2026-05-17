import tkinter as tk
from tkinter import ttk, messagebox

class ReportsView(tk.Frame):
    def __init__(self, master, record_controller):
        super().__init__(master)
        self._record_controller = record_controller
        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="Reportes del Sistema",
                 font=("Arial", 13, "bold")).pack(pady=(10, 5))

        report_notebook = ttk.Notebook(self)
        report_notebook.pack(fill="both", expand=True, padx=10, pady=5)

        report_notebook.add(self._build_top_recyclers_tab(report_notebook), text="Top Recicladores")
        report_notebook.add(self._build_points_status_tab(report_notebook), text="Estado de Puntos")
        report_notebook.add(self._build_materials_tab(report_notebook), text="Materiales")
        report_notebook.add(self._build_date_range_tab(report_notebook), text="Por Fecha")

    def _build_top_recyclers_tab(self, parent) -> tk.Frame:
        tab_frame = tk.Frame(parent)
        tk.Button(tab_frame, text="Generar reporte",
                  command=self._load_top_recyclers).pack(pady=8)

        columns = ("nombre", "distrito", "total_kg", "visitas")
        self._top_recyclers_table = ttk.Treeview(tab_frame, columns=columns,
                                                  show="headings", height=14)
        for col, label in [("nombre", "Nombre"), ("distrito", "Distrito"),
                           ("total_kg", "Total kg"), ("visitas", "Visitas")]:
            self._top_recyclers_table.heading(col, text=label)
            self._top_recyclers_table.column(col, width=160)

        self._top_recyclers_table.pack(fill="both", expand=True, padx=10)
        return tab_frame

    def _load_top_recyclers(self):
        self._top_recyclers_table.delete(*self._top_recyclers_table.get_children())
        try:
            # list de tuples: (full_name, district, total_kg, visit_count)
            for recycler_tuple in self._record_controller.get_top_recyclers():
                self._top_recyclers_table.insert("", "end", values=recycler_tuple)
        except Exception as report_error:
            messagebox.showerror("Error", str(report_error))

    def _build_points_status_tab(self, parent) -> tk.Frame:
        tab_frame = tk.Frame(parent)
        tk.Button(tab_frame, text="Generar reporte",
                  command=self._load_points_status).pack(pady=8)

        columns = ("nombre", "carga", "capacidad", "porcentaje", "estado")
        self._points_status_table = ttk.Treeview(tab_frame, columns=columns,
                                                  show="headings", height=14)
        for col, label in [("nombre", "Punto"), ("carga", "Carga (kg)"),
                           ("capacidad", "Capacidad (kg)"), ("porcentaje", "Ocupación %"),
                           ("estado", "Estado")]:
            self._points_status_table.heading(col, text=label)
            self._points_status_table.column(col, width=140)

        self._points_status_table.pack(fill="both", expand=True, padx=10)
        return tab_frame

    def _load_points_status(self):
        self._points_status_table.delete(*self._points_status_table.get_children())
        try:
            for point_status in self._record_controller.get_collection_points_status():
                self._points_status_table.insert("", "end", values=(
                    point_status["name"],
                    point_status["current_load"],
                    point_status["max_capacity"],
                    f"{point_status['percentage']}%",
                    point_status["status"]
                ))
        except Exception as report_error:
            messagebox.showerror("Error", str(report_error))

    def _build_materials_tab(self, parent) -> tk.Frame:
        tab_frame = tk.Frame(parent)
        tk.Button(tab_frame, text="Generar reporte",
                  command=self._load_materials).pack(pady=8)

        columns = ("material", "total_kg")
        self._materials_table = ttk.Treeview(tab_frame, columns=columns,
                                              show="headings", height=14)
        self._materials_table.heading("material", text="Material")
        self._materials_table.heading("total_kg", text="Total kg")
        self._materials_table.column("material", width=220)
        self._materials_table.column("total_kg", width=160)

        self._materials_table.pack(fill="both", expand=True, padx=10)
        return tab_frame

    def _load_materials(self):
        self._materials_table.delete(*self._materials_table.get_children())
        try:
            for material_name, total_kg in self._record_controller.get_materials_breakdown().items():
                self._materials_table.insert("", "end", values=(material_name, total_kg))
        except Exception as report_error:
            messagebox.showerror("Error", str(report_error))

    def _build_date_range_tab(self, parent) -> tk.Frame:
        tab_frame = tk.Frame(parent)

        filter_frame = tk.Frame(tab_frame)
        filter_frame.pack(pady=8)

        tk.Label(filter_frame, text="Fecha inicio (YYYY-MM-DD):").grid(row=0, column=0, padx=5)
        self._start_date_entry = tk.Entry(filter_frame, width=14)
        self._start_date_entry.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Fecha fin (YYYY-MM-DD):").grid(row=0, column=2, padx=5)
        self._end_date_entry = tk.Entry(filter_frame, width=14)
        self._end_date_entry.grid(row=0, column=3, padx=5)

        tk.Button(filter_frame, text="Buscar",
                  command=self._load_date_range).grid(row=0, column=4, padx=8)

        self._date_range_total_label = tk.Label(tab_frame, text="Total kg en el período: —")
        self._date_range_total_label.pack(pady=3)

        columns = ("reciclador", "punto", "material", "peso", "fecha")
        self._date_range_table = ttk.Treeview(tab_frame, columns=columns,
                                               show="headings", height=12)
        for col, label in [("reciclador", "Reciclador"), ("punto", "Punto"),
                           ("material", "Material"), ("peso", "Peso (kg)"), ("fecha", "Fecha")]:
            self._date_range_table.heading(col, text=label)
            self._date_range_table.column(col, width=140)

        self._date_range_table.pack(fill="both", expand=True, padx=10)
        return tab_frame

    def _load_date_range(self):
        start_date = self._start_date_entry.get().strip()
        end_date   = self._end_date_entry.get().strip()

        if not start_date or not end_date:
            messagebox.showwarning("Campos vacíos", "Ingresá ambas fechas para filtrar.")
            return

        self._date_range_table.delete(*self._date_range_table.get_children())
        try:
            result = self._record_controller.get_records_by_date_range(start_date, end_date)
            for record_dict in result["records"]:
                self._date_range_table.insert("", "end", values=(
                    record_dict["recycler_name"],
                    record_dict["point_name"],
                    record_dict["material"],
                    record_dict["weight"],
                    record_dict["date"]
                ))
            self._date_range_total_label.config(
                text=f"Total kg en el período: {result['total_period_kg']} kg"
            )
        except ValueError as validation_error:
            messagebox.showerror("Error de validación", str(validation_error))
        except Exception as report_error:
            messagebox.showerror("Error", str(report_error))