from InputFunctionForCsv import read_csv_file
from MakeGraphFromLists import plot_graph
from scipy import stats, interpolate

[cdeformation, cforce, ctravel, csg1, cttime] = read_csv_file('compliance.csv')
ncdeformation =[]
ncforce = []
for i in range(len(cdeformation)):
  if cdeformation[i]>=0.5:
    ncdeformation.append(cdeformation[i])
    ncforce.append(cforce[i]+2043.7124945319065)
#slope, intercept, r_value, p_value, std_err = stats.linregress(ncdeformation, ncforce)
Compliance_funct = interpolate.interp1d(y_point, cllst, kind='cubic', fill_value='extrapolate')
#Slope = 9377.214897701953