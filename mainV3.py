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
    color_lst = ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2']
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
avg_strain10=[]
avg_stress10=[]
thickness50 = [2.78, 2.91, 2.98, 2.73] 
avg_strain50=[]
avg_stress50=[]
thickness20 = [2.73, 2.63, 2.63, 2.72]
avg_strain20=[]
avg_stress20=[]
thicknessTNB = [2.5, 2.49, 2.52, 2.53]
avg_strainTNB=[]
avg_stressTNB=[]
thicknessNBM = [2.69, 2.37, 2.36, 2.34]
avg_strainNBM=[]
avg_stressNBM=[]
widthNBM = [15, 15, 15, 15]
width10 = [15, 15, 15, 15]
width50 = [12.1, 12.13, 12.07, 12.11]
width20 = [12, 12.15, 12.1, 12.07]
widthTNB = [11.97, 11.9, 11.91, 12.07]

#clear the results file
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
        def averages():
            if checker=='1':
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
            if checker=='\\':
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
            if checker=='2':
                if len(avg_strain20)>=len(strain):
                    for o in range(len(strain)):
                        avg_strain20[o]+=strain[o]
                else:
                    alen = len(avg_strain20)
                    for o in range(len(avg_strain20)):
                        avg_strain20[o]+=strain[o]
                    for p in range(len(strain)-len(avg_strain20)):
                        avg_strain20.append(strain[alen+p])
                if len(avg_stress20)>=len(stress):
                    for o in range(len(stress)):
                        avg_stress20[o]+=stress[o]
                else:
                    alen = len(avg_stress20)
                    for o in range(len(avg_stress20)):
                        avg_stress20[o]+=stress[o]
                    for p in range(len(stress)-len(avg_stress20)):
                        avg_stress20.append(stress[alen+p])
            elif checker=='5':
                if len(avg_strain50)>=len(strain):
                    for o in range(len(strain)):
                        avg_strain50[o]+=strain[o]
                else:
                    alen = len(avg_strain50)
                    for o in range(len(avg_strain50)):
                        avg_strain50[o]+=strain[o]
                    for p in range(len(strain)-len(avg_strain50)):
                        avg_strain50.append(strain[alen+p])
                if len(avg_stress50)>=len(stress):
                    for o in range(len(stress)):
                        avg_stress50[o]+=stress[o]
                else:
                    alen = len(avg_stress50)
                    for o in range(len(avg_stress50)):
                        avg_stress50[o]+=stress[o]
                    for p in range(len(stress)-len(avg_stress50)):
                        avg_stress50.append(stress[alen+p])
            elif checker =='i':
                if len(avg_strainTNB)>=len(strain):
                    for o in range(len(strain)):
                        avg_strainTNB[o]+=strain[o]
                else:
                    alen = len(avg_strainTNB)
                    for o in range(len(avg_strainTNB)):
                        avg_strainTNB[o]+=strain[o]
                    for p in range(len(strain)-len(avg_strainTNB)):
                        avg_strainTNB.append(strain[alen+p])
                if len(avg_stressTNB)>=len(stress):
                    for o in range(len(stress)):
                        avg_stressTNB[o]+=stress[o]
                else:
                    alen = len(avg_stressTNB)
                    for o in range(len(avg_stressTNB)):
                        avg_stressTNB[o]+=stress[o]
                    for p in range(len(stress)-len(avg_stressTNB)):
                        avg_stressTNB.append(stress[alen+p])

        #comment the following line and change to false if you don't want average graphs
        #averages()
        averages_true = False

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
            text_f = open('Data\MolarChange\Results.txt', 'a')
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
    color_lst = ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2']
    label_lst = ['10mM', '20mM', '50mM', 'Treated, not biomineralized', 'Not treated']
    avg_strain10=np.array(avg_strain10)/4
    for i in range(len(avg_strain10)):
        if avg_strain10[i+1]<avg_strain10[i]:
            avg_strain10=avg_strain10[:i]
            avg_stress10=avg_stress10[:i]
            break
    avg_stress10=np.array(avg_stress10)/4
    avg_strain20=np.array(avg_strain20)/4
    for i in range(len(avg_strain20)):
        if avg_strain20[i+1]<avg_strain20[i]:
            avg_strain20=avg_strain20[:i]
            avg_stress20=avg_stress20[:i]
            break
    avg_stress20=np.array(avg_stress20)/4
    avg_strain50=np.array(avg_strain50)/4
    for i in range(len(avg_strain50)):
        if avg_strain50[i+1]<avg_strain50[i]:
            avg_strain50=avg_strain50[:i]
            avg_stress50=avg_stress50[:i]
            break
    avg_stress50=np.array(avg_stress50)/4
    avg_strainNBM=np.array(avg_strainNBM)/4
    for i in range(len(avg_strainNBM)):
        if avg_strainNBM[i+1]<avg_strainNBM[i]:
            avg_strainNBM=avg_strainNBM[:i]
            avg_stressNBM=avg_stressNBM[:i]
            break
    avg_stressNBM=np.array(avg_stressNBM)/4
    avg_strainTNB=np.array(avg_strainTNB)/4
    for i in range(len(avg_strainTNB)):
        if avg_strainTNB[i+1]<avg_strainTNB[i]:
            avg_strainTNB=avg_strainTNB[:i]
            avg_stressTNB=avg_stressTNB[:i]
            break
    avg_stressTNB=np.array(avg_stressTNB)/4

    #comment or uncomment the following 5 lines depending on what you would like the graph to look like
    plt.plot(avg_strain10, avg_stress10, label = label_lst[0], color = color_lst[0])
    plt.plot(avg_strain20, avg_stress20, label = label_lst[1], color = color_lst[1])
    plt.plot(avg_strain50, avg_stress50, label = label_lst[2], color = color_lst[2])
    plt.plot(avg_strainTNB, avg_stressTNB, label = label_lst[3], color = color_lst[3])
    plt.plot(avg_strainNBM, avg_stressNBM, label = label_lst[4], color = color_lst[4])
    plt.xlabel('Strain[-]')
    plt.ylabel('Stress[Pa]')
    plt.title('Stress Strain Graph Averages for Compression')
    plt.grid(True)
    plt.legend(loc ="lower right", ncol = 2)
    plt.savefig('Averages')
