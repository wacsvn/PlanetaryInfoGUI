import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import Listbox, Scrollbar, Text, END, ttk

# URL of the webpage to scrape
url = "https://nssdc.gsfc.nasa.gov/planetary/factsheet/planet_table_ratio.html"
response = requests.get(url)

# check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')

    # initialize a dictionary to store planet data by property name
    planet_data = {}

    # initialize list of properties key = property name value = that row
    properties = []

    # extract the planet names from the table headers
    planet_names = [header.text.strip() for header in table.find_all('td')[1:11]]

    # loop through the rows in the table, excluding the first row
    rows = table.find_all('tr')[1:19]
    for row in rows:
        columns = row.find_all('td')

        # extract the data for each column in the row
        row_data = [column.text.strip() for column in columns]
        properties.append(row_data)

    # populate planet_data with key = planet and value = list of properties
    for i in range(10):
        value = []
        planet_name = planet_names[i]
        for property in properties:
            value.append(property[i + 1])
        planet_data[planet_name] = value

    # Now, planet_data contains the data organized by property name
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)

"""
Planet Class
"""
class Planet:
    def __init__(self, name, mass_ratio, diameter_ratio, density_ratio, gravity_ratio, escape_velocity, rotation_period,
                 length_of_day, distance_from_sun, perihelion, aphelion, orbital_period, orbital_velocity,
                 orbital_eccentricity, obliquity_to_orbit, surface_pressure, number_of_moons, ring_system,
                 global_magnetic_field):
        self.name = name
        self.mass_ratio = mass_ratio
        self.diameter_ratio = diameter_ratio
        self.density_ratio = density_ratio
        self.gravity_ratio = gravity_ratio
        self.escape_velocity = escape_velocity
        self.rotation_period = rotation_period
        self.length_of_day = length_of_day
        self.distance_from_sun = distance_from_sun
        self.perihelion = perihelion
        self.aphelion = aphelion
        self.orbital_period = orbital_period
        self.orbital_velocity = orbital_velocity
        self.orbital_eccentricity = orbital_eccentricity
        self.obliquity_to_orbit = obliquity_to_orbit
        self.surface_pressure = surface_pressure
        self.number_of_moons = number_of_moons
        self.ring_system = ring_system
        self.global_magnetic_field = global_magnetic_field

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Planet('{self.name}')"

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        return self.name == other.name

"""
Planet GUI
"""
class PlanetInfoApp:
    def __init__(self, planet_data):
        self.planet_data = planet_data

        # window creation
        self.window = tk.Tk()
        self.window.title("Planetary Fact Sheet - Ratio to Earth Values")
        self.window.configure(bg="#111")

        # customize colors
        style = ttk.Style()
        style.configure("TLabel", background="#111", foreground="white")
        style.configure("TFrame", background="#111")
        style.configure("TButton", background="#008CBA", foreground="white")

        # listbox: pane on left to display planets of choice
        self.planet_listbox = tk.Listbox(self.window, selectmode=tk.SINGLE, width=19, height=19, bg="#111",
                                         selectforeground="white", fg="white", selectbackground="blue",
                                         font=("Arial", 15))
        for planet in self.planet_data.keys():
            self.planet_listbox.insert(tk.END, planet)
        self.planet_listbox.pack(side=tk.LEFT)

        # display the planet information
        self.planet_info_text = tk.Text(self.window, width=30, height=19, bg="#111", fg="white",
                                        font=("Arial", 16))
        self.planet_info_text.pack(side=tk.LEFT)

        # bind Listbox selection with planet information
        self.planet_listbox.bind("<<ListboxSelect>>", self.show_planet_info)

    # when triggered, displays the info for that planet
    def show_planet_info(self, event):
        selected_planet = self.planet_listbox.get(self.planet_listbox.curselection())
        if selected_planet in self.planet_data:
            self.planet_info_text.delete(1.0, tk.END)  # Clear the existing text
            for property_name, value in zip(properties, self.planet_data[selected_planet]):
                self.planet_info_text.insert(tk.END, f"{property_name[0]}: {value}\n")

if __name__ == "__main__":
    planet_info_app = PlanetInfoApp(planet_data)
    planet_info_app.run()

    def run(self):
        self.window.mainloop()
