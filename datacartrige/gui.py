import tkinter
import customtkinter
import tkintermapview
import parsers
from PIL import ImageTk
from os import listdir
from os.path import isfile, join

class DragDropListbox(tkinter.Listbox):
    """ A Tkinter listbox with drag'n'drop reordering of entries. """
    def __init__(self, master, **kw):
        kw['selectmode'] = tkinter.SINGLE
        tkinter.Listbox.__init__(self, master, kw)
        self.bind('<Button-1>', self.setCurrent)
        self.bind('<B1-Motion>', self.shiftSelection)
        self.curIndex = None

    def setCurrent(self, event):
        self.curIndex = self.nearest(event.y)

    def shiftSelection(self, event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i+1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i-1, x)
            self.curIndex = i

class Gui(customtkinter.CTk):
    WIDTH = 1000
    HEIGHT = 600
    NAME = "DTC TOOL"

    THEATER_PATH = "data"

    # TODO obj_icon = ImageTk.PhotoImage()
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

        self.title(self.NAME)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.minsize(self.WIDTH, self.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        ### Variables 
        
        self.bf_parser = parsers.BF_CSV_Parser("data/Caucasus_80s_Objectives.csv")
        self.selected_wp_name = tkinter.StringVar(value=["Kazbegi", "Beslan", "Java"])
        self.objective_names = tkinter.StringVar(value=self.bf_parser.objective_names)

        self.message = tkinter.StringVar()

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

        self.wp_panel.grid_rowconfigure(6, weight=1)

        customtkinter.CTkLabel(self.dtc_panel, text="Aircraft").grid(row=0, column=0, sticky="sw", padx=(12, 12))
        self.aircraft_select = customtkinter.CTkOptionMenu(self.dtc_panel, values=["M2000-C"])
        self.aircraft_select.grid(row=1, column=0, padx=(12,12), pady=(0, 6))

        customtkinter.CTkLabel(self.dtc_panel, text="Terrain").grid(row=2, column=0, sticky="sw", padx=(12, 12))
        self.terrain_select = customtkinter.CTkOptionMenu(self.dtc_panel, values=self.get_available_theaters(), command=self.on_theater_selected)
        self.terrain_select.grid(row=3, column=0, padx=(12,12), pady=(0, 6))

        customtkinter.CTkLabel(self.dtc_panel, text="Name").grid(row=4, column=0, sticky="sw", padx=(12, 12))
        self.name_entry = customtkinter.CTkEntry(master=self.dtc_panel,
                                            placeholder_text="Cartridge name...")
        self.name_entry.grid(row=5, column=0, sticky="we", padx=(12, 12), pady=(0,6))

        self.wp_listbox = DragDropListbox(self.dtc_panel, height=15, listvariable=self.selected_wp_name)
        self.wp_listbox.grid(row=6, column=0, padx=(12, 12), pady=(0,6), sticky="nsew")


        self.export_button = customtkinter.CTkButton(self.dtc_panel, 
                                                text="Export", 
                                                command=self.export)
        self.export_button.grid(column=0, row=10, padx=12, pady = 12, sticky="s")

        ### Waypoint selection panel

        self.wp_panel.grid_rowconfigure(1, weight=1)

        self.entry = customtkinter.CTkEntry(master=self.wp_panel,
                                            placeholder_text="waypoint name...")
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", self.search)

        self.search_button = customtkinter.CTkButton(master=self.wp_panel,
                                                text="Search",
                                                width=90,
                                                command=self.search)
        self.search_button.grid(row=0, column=1, sticky="w", padx=(0, 12), pady=12)

        self.objectives_listbox = tkinter.Listbox(self.wp_panel, height=30, 
                                               listvariable=self.objective_names)
        self.objectives_listbox.grid(row=1, column=0, columnspan=2, padx=(12,12), pady=(12,12), sticky="nsew")


        ### Map panel
        
        self.map_view()
        
        ### Error bar
        
        self.error_bar = customtkinter.CTkLabel(self, textvariable=self.message)
        self.error_bar.grid(column=0, row=1, columnspan=3, sticky="sw", padx=12) 

    def export(self):
        self.message.set("Exporting...")

    def search(self, event=None):
        self.message.set("Searching...")

    def map_view(self):
        self.map_widget = tkintermapview.TkinterMapView(self, corner_radius=0)
        self.map_widget.grid(column=2, row=0, sticky="nswe")
        self.center_map()
        self.map_widget.set_tile_server("http://a.tile.stamen.com/toner/{z}/{x}/{y}.png")  # black and white
        self.draw_map()

    def draw_map(self):
        for obj in self.bf_parser.objective_list:
            self.map_widget.set_marker(obj.coords.deg_lat, obj.coords.deg_long, text=obj.name)
    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()

    def on_theater_selected(self, choice):
        self.bf_parser = parsers.BF_CSV_Parser(join(self.THEATER_PATH, f"{choice}"))
        self.map_widget.delete_all_marker()
        self.draw_map()
        self.center_map()

    def get_available_theaters(self):
        return [f for f in listdir(self.THEATER_PATH) if isfile(join(self.THEATER_PATH, f)) and f.endswith('.csv')]

    def center_map(self):
        ax = [f.coords.deg_long for f in self.bf_parser.objective_list]
        ay = [f.coords.deg_lat for f in self.bf_parser.objective_list]

        mx = sum(ax)/len(ax)
        my = sum(ay)/len(ay)

        self.map_widget.set_position(my, mx)
        self.map_widget.set_zoom(7)