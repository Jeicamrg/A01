from InputFunctionForCsv import read_csv_file
from MakeGraphFromLists import plot_graph, bplot_graph
from scipy import stats, interpolate
from scipy.stats import linregress
import scipy
import numpy as np
import matplotlib.pyplot as plt
#FILE COMMANDS
file = 'nbm3'
ftype = 'Data\Tensile\\'
file2 =  ftype + file + '.csv'
dtype = ftype[5]


#READING THE DATA
if dtype=='C':
  deformation, force, travel, sg1, ttime = read_csv_file(file2)
elif dtype=='F':
  deformation, force, travel, crosshead, ttime = read_csv_file(file2)
elif dtype=='T':
  force, gtg, deformation, ttime = read_csv_file(file2)
else:
  print('You probably have the wrong folder')


#COMPLIANCE
if dtype=='C':
  [cdeformation, cforce, ctravel, csg1, cttime] = read_csv_file('Data\Compressive\compliance.csv')
  ncdeformation =[]
  ncforce = []
  for i in range(len(cdeformation)):
    if cdeformation[i]>=0.5:
      ncdeformation.append(cdeformation[i])
      ncforce.append(cforce[i])
      Compliance_funct = interpolate.interp1d(ncforce, ncdeformation, kind='linear', fill_value='extrapolate')
else:
  print('No compliance')
  ncforce = []
  ncdeformation = []
  for i in range(len(deformation)):
    ncforce.append(force[i])
    ncdeformation.append(0)
  Compliance_funct = interpolate.interp1d(ncforce, ncdeformation, kind='linear', fill_value='extrapolate')


#THICKNESS
if dtype=='C':
  thickness_lst = [2.65, 2.73, 2.56, 2.71, 2.3, 2.69, 2.71, 2.37, 2.36, 2.34]
elif dtype=='F':
  thickness_lst = [2.63, 2.67, 2.61, 2.85, 2.28, 2.29, 2.28, 2.23]
elif dtype=='T':
  thickness_lst = [1.68, 1.8, 1.72, 1.7, 1.4, 1.42, 1.29, 1.64]
else:
  print('You probably have the wrong folder')

if file[0] == 'b':
  t = thickness_lst[int(file[-1])-1]
elif file[0] == 'n':
  t = thickness_lst[int(file[-1])+3]
else:
  t = 2
  print('Thickness error')


#NORMALIZING THE DATA WITH COMPLIANCE
A = 0.015*t/1000#m^2 
original_l = 0.14 #m
stress = []
strain = []

for j in range(len(deformation)):
  strain.append((deformation[j]-Compliance_funct(force[j]))/(original_l*1000))
  stress.append(force[j]/(A))
mstrain = min(strain)
mstrain = abs(mstrain)
for k in range(len(strain)):
  strain[k] = strain[k]+mstrain

#for plotting stress strain grph
bplot_graph(strain, stress, file, ftype)


#############################################################################################################
#Actual calcualtions below
def calculate_ult_tens(stress):
  stress = np.array(stress)
  ult_t = np.max(stress)
  return ult_t

def tangent_stiffness(strain, stress):
  def slope(x, y):
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    return dy / dx if dx != 0 else float('inf')  
  
  tangent_lines = []
  for i in range(len(strain)-1):
    x =[]
    y=[]
    x.append(strain[i])
    x.append(strain[i+1])
    y.append(stress[i])
    y.append(stress[i+1])
    m = slope(x, y) 
    if m>10**(11): #patch to prevent infinities
      tangent_lines.append(0)
      continue
    tangent_lines.append(m)

  #for plotting tangents
  def tanplot():
    plt.plot(strain[11:], tangent_lines[10:])
    plt.xlabel('Strain[-]')
    plt.ylabel('Young\'s Modulus [Pa]')
    plt.title('Young\'s Modulus Strain Graph')
    plt.grid(True)
    plt.savefig('Tangents' +'.png')
  #tanplot()
  max_tan = max(tangent_lines)/(10**9)#convert to GPa

  #for plotting the Young's modulus to make sure it makes sense
  def sanity_check():
    sanity=[]
    for i in range(len(strain)-1):
      sanity.append(max_tan*(10**9)*strain[i])
    tot_len = int(((len(strain)/3)+1))
    plt.plot(strain[11:tot_len], sanity[10:tot_len-1])
    plt.xlabel('Strain[-]')
    plt.ylabel('Young\'s Modulus [Pa]')
    plt.title('Young\'s Modulus Strain Graph')
    plt.grid(True)
    plt.savefig('Sanity' +'.png')
  #sanity_check()
  return max_tan


def calculate_toughness(strain, stress):
  strain = np.array(strain)
  stress = np.array(stress)
  area = np.trapz(stress,strain)
  return area



#print('Youngs modulus = ', tangent_stiffness(strain, stress))
#print('Ult tens = ', calculate_ult_tens(stress)/(10**6))
#print('Toughness = ', calculate_toughness(strain, stress)/1000000)