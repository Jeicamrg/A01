import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.spatial import cKDTree
import os

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

    

def standardize(lst,std,mean):
    
    for i in lst:
        
        i = (i-mean)/std
    
    return lst


def area(file,threshold,threshold2,pix,img):

    df = pd.read_excel(file)

    area = df['Area'][1:].tolist()
    area2 = []
    for i in area:
        if i < threshold and i > threshold2:
            area2.append(i)
    
    
    X_data = df['X'][1:].tolist()
    Y_data = df['Y'][1:].tolist()
    
    x_axis, y_axis = axis_image(img)
    X_std = []
    Y_std = []
    for i in X_data:
        X_std.append(np.abs(i-x_axis))
        
    for j in Y_data:
        Y_std.append(np.abs(j-y_axis))
    
    density = nearest_neighbor_analysis(X_std, Y_std)

    

    return density,area2

def boxplot(lst,ind):
    
    
    plt.boxplot(lst, showfliers=False)

    plt.ylabel('Mineral Area (#pixels)')

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
    sizes = []
    densities = []
    lst = get_data(path2)
    for folder in os.listdir(path):
        folder_path = os.path.join(path, folder)
        
        idx = os.listdir(path).index(folder)
        if os.path.isdir(folder_path):
            
            density2 = []
            sizes2 = []
            concentration_lst2 = []
            for file in os.listdir(folder_path):
                idx2 = os.listdir(folder_path).index(file)
                
                file_path = os.path.join(folder_path, file)

                width,height = axis_image(file_path)
                size = width*height*4
                sizes2.append(size)
                density,mineral = area(lst[idx][idx2],3000,10,size,file_path)
                density2.append(density)
                for i in mineral:
                    concentration_lst2.append(i)
            
            densities.append(density2)
            concentration_lst.append(concentration_lst2)
            sizes.append(sizes2)
            
    return concentration_lst,sizes,densities


def get_info(lst,lst2,lst3):
    final_data = []

    for i in lst:
        idx = lst.index(i)
        area_perc = sum(lst[idx])/sum(lst2[idx])*100
        count = len(i)
        density = np.mean(lst3[idx]) 
        final_data.append([idx,area_perc,count,density])
        
        boxplot(i,idx)
        
    return final_data


script_dir = os.path.dirname(os.path.abspath(__file__))


path1 = os.path.join(script_dir, "Actual_images")
path2 = os.path.join(script_dir, "Data_SEM")

print(get_info(measure(path1,path2)[0],measure(path1,path2)[1],measure(path1,path2)[2]))

