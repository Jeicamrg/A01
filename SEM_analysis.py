import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.spatial import cKDTree
import os


conversion = 1174664.587/25400



def axis_image(file):
    image = Image.open(file)
    width,height = image.size
    width = width/2
    height = height/2

    return width,height

def remove_outliers(data):

    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    

    iqr = q3 - q1
    
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    

    data_no_outliers = [x for x in data if lower_bound <= x <= upper_bound]
    
    return data_no_outliers

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

    plt.ylabel('Mineral Diameter [$\mu$m]')
    
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
                    i = i/conversion
                    concentration_lst2.append(i)
                    
            
            
            
            densities.append(density2)
            concentration_lst.append(concentration_lst2)
            sizes.append(sizes2)
            
    return concentration_lst,sizes,densities


def get_info(lst,lst2,lst3):
    final_data = []
    sizes = []

    for i in lst:
        idx = lst.index(i)
        print(min(i))
        
        
        area_perc = sum(lst[idx])/(sum(lst2[idx])/conversion)*100
        count = len(remove_outliers(i))
        density = np.mean(lst3[idx]) 
        avg = np.mean(i)
        final_data.append([idx,area_perc,count,density,avg])

        rounded_list = [round(x/0.5)*0.5 for x in i]
        print(np.mean(rounded_list))
        
        value_counts = {}
        for value in rounded_list:
            if value in value_counts:
                value_counts[value] += 1
            else:
                value_counts[value] = 1
                
        

        # Extract values and counts
        values = list(value_counts.keys())
        counts = list(value_counts.values())
        
        counts = standardize(counts, np.std(counts), np.mean(counts))
        
        
        plt.hist(i,bins=100,density=False)
        plt.xlabel('Particle Size [$\mu$m]')
        plt.ylabel('Count')
        plt.show()
    boxplot(lst,idx)
    
     
    sizes = lst
        
    return final_data,sizes


script_dir = os.path.dirname(os.path.abspath(__file__))


path1 = os.path.join(script_dir, "Actual_images")
path2 = os.path.join(script_dir, "Data_SEM")

Final_data = get_info(measure(path1,path2)[0],measure(path1,path2)[1],measure(path1,path2)[2])
print(Final_data[0])



X_10 = np.arange(0,len(remove_outliers(Final_data[1][0])),1)
X_20 = np.arange(0,len(remove_outliers(Final_data[1][1])),1)
X_50 = np.arange(0,len(remove_outliers(Final_data[1][2])),1)

plt.plot(X_10,sorted(remove_outliers(Final_data[1][0]), reverse=True),color = '#E69F00',label='10mM')
plt.plot(X_20,sorted(remove_outliers(Final_data[1][1]),reverse=True),color = '#56B4E9',label='20mM')
plt.plot(X_50,sorted(remove_outliers(Final_data[1][2]),reverse=True),color = '#009E73',label='50mM')
plt.xlabel('Particle Count')
plt.ylabel('Particle Diameter [$\mu$m]')

plt.legend(loc='upper right')
plt.grid(True)
plt.show() 