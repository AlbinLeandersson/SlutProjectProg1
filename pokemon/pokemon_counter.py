import pandas as pd
import PySimpleGUI as sg

# Set the theme
sg.theme('DarkBlue2')

# Loading the Pokémon dataset
poke = pd.read_csv("Pokemon.csv")

# Define the layout
layout = [
    [sg.Text("Pokemon Counter Calculator", font=("Helvetica", 20), justification="center", pad=((0,0),(10,0)))],
    [sg.Text("Enter the name of your pokemon:", font=("Helvetica", 14), pad=((10,0),(0,10)))],
    [sg.Input(key="-INPUT-", font=("Helvetica", 14), size=(20,1), pad=((0,10),(0,10)))],
    [sg.Button("Submit", font=("Helvetica", 14), pad=((10,0),(0,10))), sg.Button("Exit", font=("Helvetica", 14), pad=((0,10),(0,10)))],
    [sg.Text("Your Pokemon", font=("Helvetica", 14), pad=((10,0),(20,0)))],
    [sg.Table(values=[], headings=["Name", "Total", "Type 1", "Type 2"], key="-USER_TABLE-", num_rows=1, row_height=30, enable_events=True, auto_size_columns=False, col_widths=[20,10,10,10], font=("Helvetica", 12), justification="center", pad=((10,10),(0,20)))],
    [sg.Text("Counter Pokemon", font=("Helvetica", 14), pad=((10,0),(0,10)))],
    [sg.Table(values=[], headings=["Name", "Total", "Type 1", "Type 2"], key="-COUNTER_TABLE-", num_rows=6, row_height=30, enable_events=True, auto_size_columns=False, col_widths=[20,10,10,10], font=("Helvetica", 12), justification="center", pad=((10,10),(0,10)))],
]

# Create the window
window = sg.Window("Pokemon Counter Calculator", layout, size=(600, 500), keep_on_top=True, no_titlebar=True, grab_anywhere=True, alpha_channel=.98)

while True:
    event, values = window.read()
    
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    
    if event == "Submit":
        # Finding the user's pokemon type, weaknesses, and total stats
        usr_poke = values["-INPUT-"].capitalize() if values["-INPUT-"].islower() else values["-INPUT-"]
        usr_type1 = poke.loc[poke['Name'] == usr_poke, 'Type 1'].values[0]
        usr_type2 = poke.loc[poke['Name'] == usr_poke, 'Type 2'].values[0]
        usr_total = poke.loc[poke['Name'] == usr_poke, 'Total'].values[0]

        # Updating the user table with the user's pokemon stats
        table_data = [[usr_poke, usr_total, usr_type1, usr_type2]]
        window["-USER_TABLE-"].update(values=table_data)

        weakness = []
        for t in [usr_type1, usr_type2]:
            if t:
                if t == 'Fire':
                    weakness += ['Water', 'Ground', 'Rock', 'Dragon', 'Fire']
                elif t == 'Water':
                    weakness += ['Electric', 'Grass', 'Dragon', 'Water']
                elif t == 'Grass':
                    weakness += ['Fire', 'Ice', 'Poison', 'Flying', 'Bug', 'Grass']
                elif t == 'Electric':
                    weakness += ['Ground', 'Electric']
                elif t == 'Ice':
                    weakness += ['Fire', 'Fighting', 'Rock', 'Steel', 'Ice']
                elif t == 'Fighting':
                    weakness += ['Flying', 'Psychic', 'Fairy']
                elif t == 'Poison':
                    weakness += ['Ground', 'Psychic', 'Poison']
                elif t == 'Ground':
                    weakness += ['Water', 'Grass', 'Ice']
                elif t == 'Flying':
                    weakness += ['Electric', 'Ice', 'Rock']
                elif t == 'Psychic':
                    weakness += ['Bug', 'Ghost', 'Dark', 'Psychic']
                elif t == 'Bug':
                    weakness += ['Fire', 'Flying', 'Rock']
                elif t == 'Rock':
                    weakness += ['Water', 'Grass', 'Fighting', 'Ground', 'Steel']
                elif t == 'Ghost':
                    weakness += ['Dark']
                elif t == 'Dragon':
                    weakness += ['Ice', 'Dragon', 'Fairy']
                elif t == 'Dark':
                    weakness += ['Fighting', 'Bug', 'Fairy']
                elif t == 'Steel':
                    weakness += ['Fire', 'Fighting', 'Ground', 'Steel']
                elif t == 'Fairy':
                    weakness += ['Poison', 'Steel']

        # Finding the counter pokemons
        counter = {}
        for i, row in poke.iterrows():
            name = row['Name']
            types = [row['Type 1'], row['Type 2']]
            total = row['Total']
            if name not in weakness:
                # Add some restrictions to get variety of pokemons calculated
                if total > usr_total - 50 and total < usr_total + 100:
                    counter[name] = total

        # Sorting the counter pokemons by total stats and getting the top 10
        counter = dict(sorted(counter.items(), key=lambda x: x[1], reverse=True)[:10])

        # Creating a list of lists for the counter pokemon table
        table_data = [[name, poke.loc[poke['Name'] == name, 'Total'].values[0], 
                       poke.loc[poke['Name'] == name, 'Type 1'].values[0], 
                       poke.loc[poke['Name'] == name, 'Type 2'].values[0]] 
                      for name in counter.keys()]

        # Update the counter pokemon table
        window['-COUNTER_TABLE-'].update(values=table_data)

window.close()