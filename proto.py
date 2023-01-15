import tkinter
import tkintermapview
import customtkinter
import os


class Waypoint():
    def __init__(self, coords) -> None:
        self.coords = coords


class App(customtkinter.CTk):

    APP_NAME = "DCS Map prototype"
    WIDTH = 800
    HEIGHT = 750

    waypoints = list()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # create tkinter window
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.title(self.APP_NAME)

        # create map widget
        self.map_widget = tkintermapview.TkinterMapView(self, width=self.WIDTH, height=self.HEIGHT, corner_radius=0)
        self.map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        
        self.map_widget.set_tile_server("http://a.tile.stamen.com/toner/{z}/{x}/{y}.png")  # black and white

        # set current widget position and zoom
        self.map_widget.set_position(43, 42)  # Caucasus
        # map_widget.fit_bounding_box()
        self.map_widget.set_zoom(7)
            
        self.map_widget.add_left_click_map_command(self.add_marker_event)

    def add_marker_event(self, coords):
        print("Add marker:", coords)
        self.waypoints.append(Waypoint(coords))
        new_marker = self.map_widget.set_marker(coords[0], coords[1], text=f"{len(self.waypoints)}")

    def start(self):
        self.mainloop()

if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")
    app = App()
    app.start()