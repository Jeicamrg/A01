import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('Data/incubation time-fabric weight salt weight.csv')


pre_biomineralization_weight = df['Pre biomineralization weight (g)'].tolist()
biomineralized_weight = df['Biomineralized weight (g)'].tolist()

time=[3,9,12,15,18,21,24] #hours as a incubation time

plt.figure()
plt.plot(time, pre_biomineralization_weight, marker='o', label='Pre-biomineralization weight')
plt.plot(time, biomineralized_weight, marker='o', label='Biomineralized weight')
plt.xlabel('Time (hours)')
plt.ylabel('Weight (g)')
plt.title('Weight vs Time')

# Add legend
plt.legend()

# Show plot
plt.grid(True)
plt.savefig('deposition.png')

difference=[]

for i in range(len(time)):
    diff = ((biomineralized_weight[i] - pre_biomineralization_weight[i]) / pre_biomineralization_weight[i]) * 100
    difference.append(diff)

print(difference)

plt.figure()
plt.plot(time, difference, label='Percentage difference (%)')
plt.xlabel('Incubation time [hours]')
plt.ylabel('Percentage difference (%)')
plt.title('Percentage difference in weight vs incubation time')
plt.legend()
plt.grid(True)
plt.savefig('percentage_difference.png')

