import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

# Input data
Density = [1800, 1712, 1800, 1830, 1643, 1920, 1880] #kg/m^3
E_Modulus = [30.9, 54.5, 39.065, 37.97, 27.97, 15.32, 72.19] #GPa, Tensile Modulus
Biom_Density = [1976.8,1829.1,1912.3, 1696.2] #kg/m^3
Biom_Emod = [45.655008, 48.05929, 40.14571, 40.03018]#GPa, Tensile Modulus
Non_Biom_Density = [2500.5, 2436.4, 2505.7, 2407.2] #kg/m^3
Non_Biom_Emod = [54.89653, 27.59863, 50.42237, 39.23931] #GPa

# Combine the data into an array of points
points = np.column_stack((Density, E_Modulus))
Biom_points = np.column_stack((Biom_Density, Biom_Emod))
Non_Biom_points = np.column_stack((Non_Biom_Density, Non_Biom_Emod))

# Function to draw an ellipse around points
def draw_ellipse_around_points(points, fill_colour, border_colour):
    # Calculate the mean of the points
    center = np.mean(points, axis=0)
    
    # Calculate the covariance matrix and its eigenvalues and eigenvectors
    cov = np.cov(points, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    
    # Width and height of the ellipse are sqrt of eigenvalues (standard deviations)
    # multiplied by a factor for scaling (to ensure the ellipse covers all points)
    width, height = 2.05 * np.sqrt(eigenvalues) * 2.05 
    
    # Calculate the angle of rotation in degrees
    angle = np.arctan2(*eigenvectors[:,0][::-1])
    angle = np.degrees(angle)
    
    # Create an ellipse
    ellipse = Ellipse(xy=center, width=width, height=height, angle=angle, 
                      edgecolor=border_colour, fc= fill_colour, alpha=0.5, lw=2)
    
    return ellipse

# Draw the ellipse
ellipse = draw_ellipse_around_points(points, border_colour='blue', fill_colour='lightblue')
Biom_ellipse = draw_ellipse_around_points(Biom_points, border_colour='lime', fill_colour='palegreen')
Non_Biom_ellipse = draw_ellipse_around_points(Non_Biom_points, border_colour='orange', fill_colour='bisque')

# Plotting
fig, ax = plt.subplots()
ax.scatter(Density, E_Modulus, color='blue', label='Glass Fiber Composites')
ax.add_patch(ellipse)
ax.scatter(Biom_Density, Biom_Emod, color='green', label='Biomineralized Samples')
ax.add_patch(Biom_ellipse)
ax.scatter(Non_Biom_Density, Non_Biom_Emod, color='orange', label='Non-Biomineralized Samples')
ax.add_patch(Non_Biom_ellipse)
#plt.scatter(Density_Actual, E_ModActual, color = 'red', label = 'Actual Value')
ax.set_xlabel('Density (kg/$m^3$)')
ax.set_ylabel('Elastic Modulus (GPa)')
#ax.set_title('Ashby Plot: Elastic Modulus vs. Density')
ax.legend(loc='lower right')
plt.grid(True)
ax.set_aspect('auto', 'datalim')
plt.show()
