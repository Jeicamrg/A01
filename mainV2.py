from InputFunctionForCsv import read_csv_file
from MakeGraphFromLists import plot_graph, bplot_graph
from scipy import stats, interpolate
import scipy
import numpy as np
import matplotlib.pyplot as plt

#COMPLIANCE
[cdeformation, cforce, ctravel, csg1, cttime] = read_csv_file('Data\Compressive\compliance.csv')

#slope, intercept, r_value, p_value, std_err = stats.linregress(ncdeformation, ncforce)
ncdeformation =[]
ncforce = []
for i in range(len(cdeformation)):
  if cdeformation[i]>=0.5:
    ncdeformation.append(cdeformation[i])
    ncforce.append(cforce[i])

Compliance_funct = interpolate.interp1d(ncforce, ncdeformation, kind='linear', fill_value='extrapolate')

#FILE COMMANDS
file = 'bm-s3'
file2 = 'Data\Compressive\\' + file + '.csv'

#NORMALIZING THE DATA WITH COMPLIANCE
A = 0.015*0.005 #m^2 change the 0.005 depending on the sample
original_l = 0.14 #m
stress = []
strain = []
deformation, force, travel, sg1, ttime = read_csv_file(file2)

#print(deformation)


for j in range(len(deformation)):
  strain.append((deformation[j]-Compliance_funct(force[j]))/(original_l*1000))
  stress.append(force[j]/A)
  #stress.append((force[j]/A))
mstrain = min(strain)
mstrain = abs(mstrain)
for k in range(len(strain)):
  strain[k] = strain[k]+mstrain

#bplot_graph(strain, stress, file)

print('First value of strain list')
print(strain[1])

#DEFINITIONS
def calculate_ult_tens(stress):
  stress = np.array(stress)

  ult_t = np.max(stress)

  return ult_t

def calculate_stiffness(strain, stress):
  strain = np.array(strain)
  stress = np.array(stress)
  strain_stress_funct = interpolate.interp1d(strain, stress, kind = 'cubic' , fill_value='extrapolate')
  stress_derivatives = []
  stress_derivatives.append(stress[1]-stress[0])
  stress_derivatives.append(stress[1]-stress[0])
  for i in range(len(stress)-2):
    k = i+1
    stress_derivatives.append(stress[k+1]-stress[k-1])
  print(stress_derivatives)
  plt.plot(strain, stress_derivatives)
  plt.xlabel('Strain[-]')
  plt.ylabel('Stress[MPa]')
  plt.title('Derivative Stress Strain Graph')
  plt.grid(True)
  
  

  plt.savefig('Derivatives' +'.png')
  
  strain = strain[5:80] #how to fix :(
  stress = stress[5:80]
  stiffnesslist = []

  for i in range(len(stress)):
    stiffnesslist.append(stress[i]/strain[i])

  stiffness = np.average(stiffnesslist)

  return stiffness

def stiffness_calc(strain, stress):
  dx_lst=[]
  dy_lst=[]
  lstrain = []
  for i in range(len(strain)):
    if strain[i]<=0.00125:
      lstrain.append(strain[i])
    else:
      break
  for i in range(len(lstrain)-1):
    dx = lstrain[i+1]-lstrain[i]
    dy = stress[i+1]-stress[i]
    dx_lst.append(dx)
    dy_lst.append(dy)
  dy_lst.append(lstrain[-1]-lstrain[-2])
  bplot_graph(lstrain[15:-1], dy_lst[15:-1], 'Derivatives2')

def calculate_toughness(strain, stress):
  strain = np.array(strain)
  stress = np.array(stress)

  area = np.trapz(stress,strain)
  
  return area


stiffness_calc(strain, stress)
#TESTING DEFINITIONS
#tensile_ultimate = calculate_ult_tens(stress)
#print("Ultimate tensile strength is", tensile_ultimate, "N per meter squared")
#stifness_test = calculate_stiffness(strain, stress)
#print("Stiffness is", stifness_test, "N per m squared")
#toughness = calculate_toughness(strain, stress)
#print("Toughness is", toughness, "N per m squared")
