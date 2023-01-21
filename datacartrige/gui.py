import tkinter
import customtkinter
import tkintermapview
import parsers
from PIL import ImageTk

class Gui(customtkinter.CTk):
    WIDTH = 1000
    HEIGHT = 600
    NAME = "DTC TOOL"

    message: str = "test error"

    # TODO obj_icon = ImageTk.PhotoImage()
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

        self.title(self.NAME)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.minsize(self.WIDTH, self.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        ### Panels creation
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.dtc_panel = customtkinter.CTkFrame(self) 
        self.dtc_panel.grid(column=0, row=0, padx=0, pady=0, sticky="nsew")

        self.wp_panel = customtkinter.CTkFrame(self) 
        self.wp_panel.grid(column=1, row=0, padx=0, pady=0, sticky="nsew")

        ### DTC panel

        self.dtc_panel.grid_rowconfigure(10, weight=0)
        self.export_button = customtkinter.CTkButton(self.dtc_panel, 
                                                text="Export", 
                                                command=lambda : self.export)
        self.export_button.grid(column=0, row=10, sticky="s")

        ### Waypoint selection panel

        self.wp_panel.grid_rowconfigure(10, weight=0)

        self.entry = customtkinter.CTkEntry(master=self.wp_panel,
                                            placeholder_text="waypoint name...")
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", self.search)

        self.search_button = customtkinter.CTkButton(master=self.wp_panel,
                                                text="Search",
                                                width=90,
                                                command=self.search)
        self.search_button.grid(row=0, column=1, sticky="w", padx=(0, 12), pady=12)

        ### Map panel
        
        self.map_view()
        
        ### Error bar
        
        self.error_bar = customtkinter.CTkLabel(self, text=self.message)
        self.error_bar.grid(column=0, row=1, columnspan=3, sticky="sw", padx=12) 

    def export(self):
        self.error_bar.setvar("sdfasdf")

    def search(self, event=None):
        self.message = "Searching..."

    def map_view(self):
        self.map_widget = tkintermapview.TkinterMapView(self, corner_radius=0)
        self.map_widget.grid(column=2, row=0, sticky="nswe")

        self.map_widget.set_position(43, 42)
        self.map_widget.set_zoom(7)
        self.map_widget.set_tile_server("http://a.tile.stamen.com/toner/{z}/{x}/{y}.png")  # black and white
        caucasus80 = parsers.BF_CSV_Parser("data/Caucasus_80s_Objectives.csv")
        for obj in caucasus80.objective_list:
            self.map_widget.set_marker(obj.coords.deg_lat, obj.coords.deg_long, text=obj.name)

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()
