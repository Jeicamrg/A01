from InputFunctionForCsv import read_csv_file
from MakeGraphFromLists import plot_graph, bplot_graph, bplot_graph2
from scipy import stats, interpolate
from scipy.stats import linregress
import scipy
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from mainV2 import calculate_ult_tens, tangent_stiffness, calculate_toughness, new_stiffness

def one_plotter(list1, list2, name):
    if len(list1) != len(list2):
        print("Error: Lists must have the same length.")
        return
    #the colors below are the teal color palette Dennis is using
    #color_lst = ['#b5d1ae', '#80ae9a', '#568b87', '#1b485e', '#122740']
    #the colors below are a nice palette imho MG
    #color_lst = ['#a559aa', '#59a89c', '#f0c571', '#e02b35', '#082a54']
    #the colors below are good for the color blind
    color_lst = ['#E69F00', '#000000']
    avg_lst = [246.6229, 318.0306]
    for an_avg in range(len(avg_lst)):
        avg_lst[an_avg] = avg_lst[an_avg]*(10**6)
    sig = name[17]
    if sig == 'm':
        color = color_lst[0]
        label = '10mM'
    else:
        color = color_lst[1]
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
    plt.xlabel('Strain[-]')
    plt.ylabel('Stress[Pa]')
    plt.grid(True)
    if name == 'Data\Tensile2\\NonBiomineralized\\nbm3.csv':
        for anumber in range(len(avg_lst)):
            plt.axhline(avg_lst[anumber], color = color_lst[anumber], linestyle = 'dashed')
            plt.text(x = 0.0075+(anumber)*0.0025, y =avg_lst[anumber]+2000000, s =(r'$\bar{\sigma}$'+' = ' + str(round(avg_lst[anumber]/(10**8), ndigits= 3))), color = color_lst[anumber])
        plt.legend(loc ="lower right", ncol = 2)
        plt.savefig('Data\Tensile2\One_Graph')

ftype = 'Data\Tensile2\\'
f10 = ftype + 'Biomineralized\\'
fNBM = ftype + 'NonBiomineralized\\'
folders = [f10, fNBM]

thickness10 = [1.68, 1.8, 1.72, 1.7]
avg_strain10=[]
avg_stress10=[]
thicknessNBM = [1.42, 1.29, 1.64]
avg_strainNBM=[]
avg_stressNBM=[]
width10 = [14.98, 14.64, 14.45, 15.39]
widthNBM = [15.13, 15.06, 15.07]


#clear the results file
open('Data\Tensile2\Results.txt', 'w').close()

for i in folders:
    listofdir = listdir(i)
    for z in listofdir:
        if z[-1]=='g':
            listofdir.remove(z)
    checker = i[-16]
    if checker=='\\':
       thickness_lst = thickness10
       width_lst = width10
       numberinfile = 4
    elif checker=='n':
       thickness_lst = thicknessNBM
       width_lst = widthNBM
       numberinfile = 3
    else:
        print('Something went wrong with widths and thicknesses')
    for j in range(numberinfile):
        file= i+str(listofdir[j])
        force, travel, deformation, sg1 = read_csv_file(file)
        t = thickness_lst[j]
        width = width_lst[j]
        #print(file[-10:-4], width, t)
        A = (width/1000)*t/1000#m^2 
        original_l = 0.14 #m
        stress = []
        strain = []
        for l in range(len(deformation)):
            strain.append((deformation[l])/(original_l*1000))
            stress.append(force[l]/(A))
        mstrain = min(strain)
        mstrain = abs(mstrain)
        for k in range(len(strain)):
            strain[k] = strain[k]+mstrain
        zero_strain = strain[0]
        for nu in range(len(strain)):
            strain[nu]-=zero_strain
        def averages():
            if checker=='\\':
                if len(avg_strain10)>=len(strain):
                    for o in range(len(strain)):
                        avg_strain10[o]+=strain[o]
                else:
                    alen=len(avg_strain10)
                    for o in range(len(avg_strain10)):
                        avg_strain10[o]+=strain[o]
                    for p in range(len(strain)-len(avg_strain10)):
                        avg_strain10.append(strain[alen+p])
                if len(avg_stress10)>=len(stress):
                    for o in range(len(stress)):
                        avg_stress10[o]+=stress[o]
                else:
                    alen=len(avg_stress10)
                    for o in range(len(avg_stress10)):
                        avg_stress10[o]+=stress[o]
                    for p in range(len(stress)-len(avg_stress10)):
                        avg_stress10.append(stress[alen+p])
            if checker=='n':
                if len(avg_strainNBM)>=len(strain):
                    for o in range(len(strain)):
                        avg_strainNBM[o]+=strain[o]
                else:
                    alen = len(avg_strainNBM)
                    for o in range(len(avg_strainNBM)):
                        avg_strainNBM[o]+=strain[o]
                    for p in range(len(strain)-len(avg_strainNBM)):
                        avg_strainNBM.append(strain[alen+p])
                if len(avg_stressNBM)>=len(stress):
                    for o in range(len(stress)):
                        avg_stressNBM[o]+=stress[o]
                else:
                    alen = len(avg_stressNBM)
                    for o in range(len(avg_stressNBM)):
                        avg_stressNBM[o]+=stress[o]
                    for p in range(len(stress)-len(avg_stressNBM)):
                        avg_stressNBM.append(stress[alen+p])

        #comment the following line and change to false if you don't want average graphs
        averages()
        averages_true = True

        #for plotting stress strain graph for each file uncomment below
        #bplot_graph2(strain, stress, file)

        #for plotting the singular file to rule them all uncomment below
        #one_plotter(strain, stress, file)

        #for plotting only specific graphs
        #sig = file[17]
        #if sig=='1' or sig=='N':
        #    one_plotter(strain, stress, file)
        def results():
            ult_tens = calculate_ult_tens(stress)/(10**6)
            youngs = new_stiffness(strain, stress)
            toughness = calculate_toughness(strain, stress)/(10**6)
            text_f = open('Data\Tensile2\Results.txt', 'a')
            text_f.write(file + '\n')
            text_f.write('Youngs modulus = ' + str(youngs)+ '\n')
            text_f.write('Ultimate compression = ' + str(ult_tens) + '\n')
            text_f.write('Toughness = ' + str(toughness)+ '\n')
            text_f.write('\n')
            text_f.close()
        
        #before uncommenting below to see the results remeber to clear the file, uncomment line 88
        results()


if averages_true:
    #the colors below are the teal color palette Dennis is using
    #color_lst = ['#b5d1ae', '#80ae9a', '#568b87', '#1b485e', '#122740']
    #the colors below are a nice palette imho MG
    #color_lst = ['#a559aa', '#59a89c', '#f0c571', '#e02b35', '#082a54']
    #the colors below are good for the color blind
    color_lst = ['#E69F00', '#000000']
    label_lst = ['10mM', 'Treated, not biomineralized']
    avg_strain10=np.array(avg_strain10)/4
    for i in range(len(avg_strain10)):
        if avg_strain10[i+1]<avg_strain10[i]:
            avg_strain10=avg_strain10[:i]
            avg_stress10=avg_stress10[:i]
            break
    avg_stress10=np.array(avg_stress10)/4
    avg_strainNBM=np.array(avg_strainNBM)/3
    for i in range(len(avg_strainNBM)):
        if avg_strainNBM[i+1]<avg_strainNBM[i]:
            avg_strainNBM=avg_strainNBM[:i]
            avg_stressNBM=avg_stressNBM[:i]
            break
    avg_stressNBM=np.array(avg_stressNBM)/3

    #comment or uncomment the following 5 lines depending on what you would like the graph to look like
    plt.plot(avg_strain10, avg_stress10, label = label_lst[0], color = color_lst[0])
    plt.plot(avg_strainNBM, avg_stressNBM, label = label_lst[1], color = color_lst[1])
    plt.xlabel('Strain[-]')
    plt.ylabel('Stress[Pa]')
    plt.grid(True)
    plt.legend(loc ="lower right", ncol = 2)
    plt.savefig('AveragesTensile')
