from InputFunctionForCsv import read_csv_file
from MakeGraphFromLists import plot_graph, bplot_graph
from scipy import stats, interpolate
from scipy.stats import linregress
import scipy
import numpy as np
import matplotlib.pyplot as plt
from os import listdir

ftype = 'Data\MolarChange\\'
f20 = ftype + '20mM\\'
f50 = ftype + '50mM\\'
fTNB = ftype + 'TreatedButNotBiomineralized\\'
folders = [f20, f50, fTNB]
thickness20 = [2.65, 2.73, 2.56, 2.71] #change the thicknesses once available
thickness50 = [2.65, 2.73, 2.56, 2.71]
thicknessTNB = [2.65, 2.73, 2.56, 2.71]

for i in folders:
    listofdir = listdir(i)
    listofdir.remove('compliance.csv')
    #Compliance
    [cdeformation, cforce, ctravel, csg1, cttime] = read_csv_file(i+'compliance.csv')
    ncdeformation =[]
    ncforce = []
    for k in range(len(cdeformation)):
        if cdeformation[k]>=0.5:
            ncdeformation.append(cdeformation[k])
            ncforce.append(cforce[k])
            Compliance_funct = interpolate.interp1d(ncforce, ncdeformation, kind='linear', fill_value='extrapolate')
    if i==f20:
       thickness_lst = thickness20
    elif i==f50:
       thickness_lst=thickness50
    else:
       thickness_lst=thicknessTNB
    for j in range(len(listofdir)):
        file= i+str(listofdir[j])
        deformation, force, travel, sg1, ttime = read_csv_file(file)
        t = thickness_lst[j]
        A = 0.015*t/1000#m^2 
        original_l = 0.14 #m
        stress = []
        strain = []
        for l in range(len(deformation)):
            strain.append((deformation[l]-Compliance_funct(force[l]))/(original_l*1000))
            stress.append(force[l]/(A))
        mstrain = min(strain)
        mstrain = abs(mstrain)
        for k in range(len(strain)):
            strain[k] = strain[k]+mstrain

        #for plotting stress strain grph
        bplot_graph(strain, stress, file, i)
