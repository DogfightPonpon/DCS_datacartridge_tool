import tkinter
import customtkinter
import tkintermapview
import parsers
from PIL import ImageTk

class Gui(customtkinter.CTk):
    WIDTH = 1000
    HEIGHT = 800
    NAME = "DTC TOOL"

    # TODO obj_icon = ImageTk.PhotoImage()
    
    def __init__(self) -> None:
        super().__init__()
        customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        
        self.map_view()

    def button_function(self):
        print("button pressed")

    def start(self):
        self.mainloop()

    def map_view(self):
        map_widget = tkintermapview.TkinterMapView(self, width=800, height=600, corner_radius=0)
        map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        map_widget.set_position(43, 42)
        map_widget.set_zoom(7)
        map_widget.set_tile_server("http://a.tile.stamen.com/toner/{z}/{x}/{y}.png")  # black and white
        caucasus80 = parsers.BF_CSV_Parser("data/Caucasus_80s_Objectives.csv")
        for obj in caucasus80.objective_list:
            map_widget.set_marker(obj.coords.deg_lat, obj.coords.deg_long, text=obj.name)
        
        
        