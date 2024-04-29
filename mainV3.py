from InputFunctionForCsv import read_csv_file
from MakeGraphFromLists import plot_graph, bplot_graph, bplot_graph2
from scipy import stats, interpolate
from scipy.stats import linregress
import scipy
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from mainV2 import calculate_ult_tens, tangent_stiffness, calculate_toughness

def one_plotter(list1, list2, name):
    if len(list1) != len(list2):
        print("Error: Lists must have the same length.")
        return
    #the colors below are the teal color palette Dennis is using
    #color_lst = ['#b5d1ae', '#80ae9a', '#568b87', '#1b485e', '#122740']
    #the colors below are a nice palette imho MG
    color_lst = ['#a559aa', '#59a89c', '#f0c571', '#e02b35', '#082a54']
    sig = name[17]
    if sig == '1':
        color = color_lst[0]
        label = '10mM'
    elif sig =='2':
        color = color_lst[1]
        label = '20mM'
    elif sig =='5':
        color = color_lst[2]
        label = '50mM'
    elif sig =='T':
        color = color_lst[3]
        label = 'Treated, not biomineralized'
    else:
        color = color_lst[4]
        label = 'Not treated'
    if sig!='N' and sig!='T':
        if name[-5]=='1':
            plt.plot(list1, list2, label = label, color=color)
        else:
            plt.plot(list1, list2, color=color)
    if sig=='N':
        if name[-5]=='2':
            plt.plot(list1, list2, label = label, color=color)
        else:
            plt.plot(list1, list2, color=color)
    if sig=='T':
        if name[-10]=='1':
            plt.plot(list1, list2, label = label, color=color)
        else:
            plt.plot(list1, list2, color=color)
    plt.xlabel('Strain[-]')
    plt.ylabel('Stress[Pa]')
    plt.title('Compressive test results for varying concentrations')
    plt.grid(True)
    if name == 'Data\MolarChange\\NBM\\nbm-s6.csv':
        plt.legend(loc ="lower right", ncol = 2)
        plt.savefig('Data\MolarChange\One_Graph')

ftype = 'Data\MolarChange\\'
f10 = ftype + '10mM\\'
f20 = ftype + '20mM\\'
f50 = ftype + '50mM\\'
fTNB = ftype + 'TreatedButNotBiomineralized\\'
fNBM = ftype + 'NBM\\'
folders = [f10, f20, f50, fTNB, fNBM]

thickness10 = [2.65, 2.73, 2.56, 2.71]
thickness50 = [2.78, 2.91, 2.98, 2.73] 
thickness20 = [2.73, 2.63, 2.63, 2.72]
thicknessTNB = [2.5, 2.49, 2.52, 2.53]
thicknessNBM = [2.69, 2.37, 2.36, 2.34]
widthNBM = [15, 15, 15, 15]
width10 = [15, 15, 15, 15]
width50 = [12.1, 12.13, 12.07, 12.11]
width20 = [12, 12.15, 12.1, 12.07]
widthTNB = [11.97, 11.9, 11.91, 12.07]

#clear the results file
#open('Data\MolarChange\Results.txt', 'w').close()

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
    checker = i[-5]
    if checker=='1':
       thickness_lst = thickness10
       width_lst = width10
    if checker=='\\':
       thickness_lst = thicknessNBM
       width_lst = widthNBM
    if checker=='2':
       thickness_lst = thickness20
       width_lst = width20
    elif checker=='5':
       thickness_lst=thickness50
       width_lst = width50
    elif checker =='i':
       thickness_lst=thicknessTNB
       width_lst = widthTNB
    for j in range(4):
        file= i+str(listofdir[j])
        deformation, force, travel, sg1, ttime = read_csv_file(file)
        t = thickness_lst[j]
        width = width_lst[j]
        #print(file[-10:-4], width, t)
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
        #for plotting stress strain graph for each file uncomment below
        #bplot_graph2(strain, stress, file)

        #for plotting the singular file to rule them all uncomment below
        one_plotter(strain, stress, file)
        #sig = file[17]
        #if sig=='1' or sig=='N':
        #    one_plotter(strain, stress, file)
        def results():
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
        
        #before uncommenting below to see the results remeber to clear the file, uncomment line 78
        #results()
