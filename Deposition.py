import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('Data/incubation time-fabric weight salt weight.csv')


pre_biomineralization_weight = df['Pre biomineralization weight (g)'].tolist()
biomineralized_weight = df['Biomineralized weight (g)'].tolist()

time=[3,9,12,15,18,21,24] #hours as a incubation time
print(pre_biomineralization_weight)
print(biomineralized_weight)




plt.plot(time, pre_biomineralization_weight, marker='o', label='Pre-biomineralization weight')
plt.plot(time, biomineralized_weight, marker='o', label='Biomineralized weight')

# Add labels and title
plt.xlabel('Time (hours)')
plt.ylabel('Weight (g)')
plt.title('Weight vs Time')

# Add legend
plt.legend()

# Show plot
plt.grid(True)
plt.savefig('deposition.png')

