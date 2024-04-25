import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('Data/UPDATED_incubation_time.csv')


pre_biomineralization_weight = df['Pre biomineralization weight (g)'].tolist()
biomineralized_weight = df['Biomineralized weight (g)'].tolist()


time=[3,6,15,17,21,24] #hours as a incubation time

plt.figure()
plt.scatter(time, pre_biomineralization_weight, marker='o', label='Pre-biomineralization weight')
plt.scatter(time, biomineralized_weight, marker='o', label='Biomineralized weight')
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

print('bhsjhbjhas')
print(biomineralized_weight[5]-pre_biomineralization_weight[5])

plt.figure()
plt.scatter(time, difference, label='Percentage difference (%)')
plt.xlabel('Incubation time [hours]')
plt.ylabel('Percentage difference (%)')
plt.title('Percentage difference in weight vs incubation time')
plt.legend()
plt.grid(True)
plt.savefig('percentage_difference.png')

#Calcium carbonate

#Molecular mass 

Ca= 40.08 #u
Cl = 35.45 #u
Mg =24.305 #u
CalciumChloride = 0.073 #g
MagnesiumChloride = 0.102 #g
urea = 2 #g
C = 12.011 #u
O = 15.999 #u
N = 14.007 #u
H = 1.0080 #u


CaCl2= Ca + 2*Cl
MgCl2= Mg + 2*Cl
MgCO3 = Mg + C + 3*O
CONH2= C+O+(N+2*H)*2

#Weight of ions 

Ca_i= CalciumChloride/CaCl2* Ca
print('Weight of calcium ions in CalciumChloride:')
print(Ca_i)

Cl_i= CalciumChloride/CaCl2 * 2 * Cl
print('Weight of chlorine ions in CalciumChloride:')
print(Cl_i)

Cl_i_2=MagnesiumChloride/MgCl2*2*Cl
print('Weight of chlorine ions in magnesium chloride:')
print(Cl_i_2)

Mg_i= MagnesiumChloride/MgCl2*Mg
print('Weight of magnesium ions in magnesium chloride:')
print(Mg_i)

MgCO3_mass= (Mg_i/Mg)*MgCO3


# if urea/CONH2 < Ca_i/Ca:
#     print('Mass of calcium carbonate:')
#     print(urea/CONH2*100)
# else:
#     print('Mass of calcium carbonate:')
#     print(Ca_i/Ca*100)

CaCO3_mass= (Ca_i/Ca)*100
print("Value test:")
print(CaCO3_mass)

total_mass= MgCO3_mass 

print('Total mass is:')
print(total_mass)


deposition_rate = []  

for i in range(len(time)):
    deposition_rate.append((biomineralized_weight[i] - pre_biomineralization_weight[i]) / (total_mass)*100) 


plt.figure()
plt.scatter(time, deposition_rate, label='Deposition rate', color='#be2596')
plt.ylim(0, 0.5)
plt.xlabel('Incubation time [hours]')
plt.ylabel('Deposition rate')
plt.title('Depositon rate over time')
plt.grid(True)
plt.legend()
plt.savefig('deposition_rate.png')


print(deposition_rate)



plt.figure()
# Plotting deposition rate
plt.scatter(time, deposition_rate, label='Deposition rate', color='#be2596')
# Plotting percentage difference
plt.scatter(time, difference, label='Percentage difference (%)')
#plt.ylim(0, max(0.5, max(deposition_rate)))  # Adjusting y-axis limit
plt.xlabel('Incubation time [hours]')
plt.ylabel('Value')
plt.title('Deposition rate and Percentage difference over time')
plt.grid(True)
plt.legend()
plt.savefig('combined_plot.png')
plt.show()
