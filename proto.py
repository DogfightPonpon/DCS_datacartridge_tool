import tkinter
from tkintermapview import TkinterMapView
import customtkinter
import os


class Waypoint():
    def __init__(self, coords) -> None:
        self.coords = coords


class App(customtkinter.CTk):

    APP_NAME = "DCS Map prototype"
    WIDTH = 1000
    HEIGHT = 750

    waypoints = list()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # create tkinter window
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.title(self.APP_NAME)

        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(2, weight=1)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Set Marker",
                                                command=self.set_marker_event)
        self.button_1.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Clear Markers",
                                                command=self.clear_marker_event)
        self.button_2.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)

        self.map_label = customtkinter.CTkLabel(self.frame_left, text="Tile Server:", anchor="w")
        self.map_label.grid(row=3, column=0, padx=(20, 20), pady=(20, 0))
        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["Stamen", "OpenStreetMap", "Google normal", "Google satellite"],
                                                                       command=self.change_map)
        self.map_option_menu.grid(row=4, column=0, padx=(20, 20), pady=(10, 10))

        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            placeholder_text="type address")
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", self.search_event)

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Search",
                                                width=90,
                                                command=self.search_event)
        self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)


        ## Default values
        self.map_widget.set_tile_server("http://a.tile.stamen.com/toner/{z}/{x}/{y}.png")  # black and white
        # set current widget position and zoom
        self.map_widget.set_position(43, 42)  # Caucasus
        # map_widget.fit_bounding_box()
        self.map_widget.set_zoom(7)
            
        self.map_widget.add_right_click_menu_command(label="Add Waypoint", command=self.add_marker_event, pass_coords=True)

    
    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())
        self.map_widget.set_zoom(10)

    def add_marker_event(self, coords):
        self.waypoints.append(self.map_widget.set_marker(coords[0], coords[1]))

    def set_marker_event(self):
        current_position = self.map_widget.get_position()
        self.waypoints.append(self.map_widget.set_marker(current_position[0], current_position[1]))

    def clear_marker_event(self):
        for marker in self.waypoints:
            marker.delete()

    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Stamen":
            self.map_widget.set_tile_server("http://a.tile.stamen.com/toner/{z}/{x}/{y}.png")  # black and white

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()

if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")
    app = App()
    app.start()