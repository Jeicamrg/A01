from InputFunctionForCsv import read_csv_file
from MakeGraphFromLists import plot_graph, bplot_graph, bplot_graph2
from scipy import stats, interpolate
from scipy.stats import linregress
import scipy
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from mainV2 import calculate_ult_tens, tangent_stiffness, calculate_toughness

ftype = 'Data\MolarChange\\'
f10 = ftype + '10mM\\'
f20 = ftype + '20mM\\'
f50 = ftype + '50mM\\'
fTNB = ftype + 'TreatedButNotBiomineralized\\'
fNBM = ftype + 'NBM\\'
folders = [f10, f20, f50, fTNB, fNBM]
#change the thicknesses and widths once available
thickness10 = [2.65, 2.73, 2.56, 2.71]
thickness20 = [2.65, 2.73, 2.56, 2.71] 
thickness50 = [2.65, 2.73, 2.56, 2.71]
thicknessTNB = [2.65, 2.73, 2.56, 2.71]
thicknessNBM = [2.69, 2.37, 2.36, 2.34]
widthNBM = [15, 15, 15, 15]
width10 = [15, 15, 15, 15]
width20 = [12, 12, 12, 12]
width50 = [12, 12, 12, 12]
widthTNB = [15, 15, 15, 15]
open('Data\MolarChange\Results.txt', 'w').close()

for i in folders:
    listofdir = listdir(i)
    listofdir.remove('compliance.csv')
    for z in listofdir:
        if z[-1]=='g':
            listofdir.remove(z)
    #Compliance
    [cdeformation, cforce, ctravel, csg1, cttime] = read_csv_file(i+'compliance.csv')
    ncdeformation =[]
    ncforce = []
    for k in range(len(cdeformation)):
        if cdeformation[k]>=0.5:
            ncdeformation.append(cdeformation[k])
            ncforce.append(cforce[k])
            Compliance_funct = interpolate.interp1d(ncforce, ncdeformation, kind='linear', fill_value='extrapolate')
    if i==f10:
       thickness_lst = thickness10
       width_lst = width10
    if i==fNBM:
       thickness_lst = thicknessNBM
       width_lst = widthNBM
    if i==f20:
       thickness_lst = thickness20
       width_lst = width20
    elif i==f50:
       thickness_lst=thickness50
       width_lst = width50
    else:
       thickness_lst=thicknessTNB
       width_lst = widthTNB
    for j in range(4):
        file= i+str(listofdir[j])
        deformation, force, travel, sg1, ttime = read_csv_file(file)
        t = thickness_lst[j]
        width = width_lst[j]
        A = (width/1000)*t/1000#m^2 
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
        #for plotting stress strain graph
        bplot_graph2(strain, stress, file)
        ult_tens = calculate_ult_tens(stress)/(10**6)
        youngs = tangent_stiffness(strain, stress)
        toughness = calculate_toughness(strain, stress)/(10**6)
        text_f = open('Data\MolarChange\Results.txt', 'a')
        text_f.write(file + '\n')
        text_f.write('Youngs modulus = ' + str(youngs)+ '\n')
        text_f.write('Ultimate compression = ' + str(ult_tens) + '\n')
        text_f.write('Toughness = ' + str(toughness)+ '\n')
        text_f.write('\n')
        text_f.close()