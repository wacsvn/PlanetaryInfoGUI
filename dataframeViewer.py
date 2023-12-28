import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
import pandas as pd

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
    df = pd.DataFrame(planet_data)
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)

"""
Planet Class
"""
class Planet:
    def __init__(self, name, mass_ratio, diameter_ratio, density_ratio,
                 gravity_ratio, escape_velocity, rotation_period,
                 length_of_day, distance_from_sun, perihelion, aphelion,
                 orbital_period, orbital_velocity,
                 orbital_eccentricity, obliquity_to_orbit, surface_pressure,
                 number_of_moons, ring_system, global_magnetic_field):
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
EXERCISE TKinterV2
    Adds onto ExerciseMatplotLib
    GUI that can display any Dataframe
"""

# Uses multi-column list box to store the data
def displayDF():
    global root

    # hide main window after button click
    root.withdraw()
    table_window = tk.Toplevel(root)
    table_window.title("Planetary Data")

    columns = list(df.columns)
    listbox = ttk.Treeview(table_window, columns=columns, show="headings")

    # populate table
    for col in columns:
        listbox.heading(col, text=col)
        listbox.column(col, width=100)

    for i, row in df.iterrows():
        values = list(row)
        listbox.insert("", "end", values=values)

    # add scrollbar
    vsb = ttk.Scrollbar(table_window, orient="vertical", command=listbox.yview)
    vsb.pack(side='right', fill='y')
    listbox.configure(yscrollcommand=vsb.set)
    listbox.pack()

    # close the main window when the table window is closed
    def on_close():
        root.destroy()

    table_window.protocol("WM_DELETE_WINDOW", on_close)

def main():
    global root
    root = tk.Tk()
    root.title("Planetary Data Viewer")

    label = tk.Label(
        root,
        text=f"Welcome to the Planetary Data Viewer!\nData from: {url}",
        font=("Arial", 12)
    )

    # padding around label
    label.pack(pady=50)
    label.pack(padx=100)

    navigate_button = tk.Button(
        root,
        text="View Planetary Table",
        command=displayDF,
        font=("Arial", 12),
        height=2,
        width=20
    )
    navigate_button.pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    main()
