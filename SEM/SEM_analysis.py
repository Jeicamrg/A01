import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.spatial import cKDTree
import os


conversion = 5.2



def axis_image(file):
    image = Image.open(file)
    width,height = image.size
    width = width/2
    height = height/2

    return width,height


def nearest_neighbor_analysis(x_coords, y_coords):

    points = np.column_stack((x_coords, y_coords))

    tree = cKDTree(points)
    

    distances, _ = tree.query(points, k=2)
    
 
    mean_nn_distance = np.mean(distances[:, 1])
    
    return mean_nn_distance

    


def area(file):

    df = pd.read_excel(file)
    

    

    area = df['Area'][1:].tolist()


    
    X_data = df['X'][1:].tolist()
    Y_data = df['Y'][1:].tolist()
    
    
    density = nearest_neighbor_analysis(X_data, Y_data)
    
    
    #plt.scatter(X_data,Y_data)
    #plt.show()
    return density,area

def boxplot(lst,ind):
    
    
    plt.boxplot(lst, showfliers=False)

    plt.ylabel('Mineral Diameter [$\mu$m]')
    
    plt.xticks(range(1, len(ind) + 1), ind)
    plt.show()
   



def get_data(path):

    files_list = []
    

    for folder in os.listdir(path):
        folder_path = os.path.join(path, folder)
        

        if os.path.isdir(folder_path):
            

            folder_files = []
            

            for file in os.listdir(folder_path):
                
        
                file_path = os.path.join(folder_path, file)
                
     
                raw_file_path = r"{}".format(file_path)
   
                folder_files.append(raw_file_path)
            
       
            files_list.append(folder_files)
    
    return files_list



   
def measure(path,path2):
    
    concentration_lst = []
   
    densities = []
    lst = get_data(path2)
    
    for i in lst:
            
            density2 = []

            concentration_lst2 = []

            for j in i:
                

                density,mineral = area(j)
                density2.append(density)
                
                for k in mineral:
                    
                    concentration_lst2.append(k)
                    
            
            
            
            densities.append(density2)
            concentration_lst.append(concentration_lst2)
    
    
    return concentration_lst,densities


def get_parameters(lst,lst2):
    final_data = []
    diameters2 = []
    res = 45444.213
    for i in lst:
        idx = lst.index(i)
        
        diameters = []
        for j in i:
            d = 2*np.sqrt(j/np.pi)
            diameters.append(d)
            
        print(min(diameters))
        print(max(diameters))
        diameters2.append(diameters)
        
        area_perc = sum(lst[idx])/(len(lst2[idx]))/res*100
        count = len(i)
        density = np.mean(lst2[idx]) 
        avg = np.mean(diameters)
        final_data.append([idx,area_perc,count,density,avg])

        
        
        plt.hist(diameters,bins=25,density=False)
        plt.xlabel('Particle Size [$\mu$m]')
        
        plt.ylabel('Count')
        plt.show()
    idx = ["10 [mM]", "20 [mM]", "50 [mM]"]
    boxplot(diameters2,idx)
    
    
    
        
    return final_data


script_dir = os.path.dirname(os.path.abspath(__file__))


path1 = os.path.join(script_dir, "Actual_images_SEM")
path2 = os.path.join(script_dir, "Data_SEM")

Final_data = get_parameters(measure(path1,path2)[0],measure(path1,path2)[1])
print(Final_data)






#d,a = area(r"C:\Users\thoma\Documents\Python\A01\Data_SEM\50mM\50mM_S1.xlsx")



#for i in range(len(a)):
#    a[i] = 2*np.sqrt(a[i]/np.pi)
    

#print(np.mean(a))



