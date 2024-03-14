from InputFunctionForCsv import read_csv_file
from MakeGraphFromLists import plot_graph, bplot_graph
from scipy import stats, interpolate

[cdeformation, cforce, ctravel, csg1, cttime] = read_csv_file('compliance.csv')

#slope, intercept, r_value, p_value, std_err = stats.linregress(ncdeformation, ncforce)
ncdeformation =[]
ncforce = []
for i in range(len(cdeformation)):
  if cdeformation[i]>=0.5:
    ncdeformation.append(cdeformation[i])
    ncforce.append(cforce[i])

Compliance_funct = interpolate.interp1d(ncforce, ncdeformation, kind='linear', fill_value='extrapolate')

file = 'bm-s1'
file2 = file + '.csv'
#Ultimate tensile strength
A = 0.1 #m^2
original_l = 0.1 #m
stress = []
strain = []
[deformation, force, travel, sg1, ttime] = read_csv_file(file2)

for j in range(len(deformation)):
  strain.append((deformation[j]-Compliance_funct(force[j]))/original_l)
  stress.append(force[j]/A)
  #stress.append((force[j]/A))
mstrain = min(strain)
mstrain = abs(mstrain)
for k in range(len(strain)):
  strain[k] = strain[k]+mstrain

bplot_graph(strain, stress, file)

#Toughness calculation
