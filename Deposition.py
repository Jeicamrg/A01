import matplotlib as plt
import pandas as pd

df = pd.read_excel('Data/incubation time-fabric weight & salt weight.xlsx')

incubation_time = data['Incubation time'].tolist()
pre_biomineralization_weight = data['Pre biomineralization weight (g)'].tolist()
biomineralized_weight = data['Biomineralized weight (g)'].tolist()

# Convert 'not measured' entries to None
biomineralized_weight = [float(w) if w != 'not measured' else None for w in biomineralized_weight]

# Print or further process the extracted data
print("Incubation Time:", incubation_time)
print("Pre Biomineralization Weight:", pre_biomineralization_weight)
print("Biomineralized Weight:", biomineralized_weight)
