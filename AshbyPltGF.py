# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 09:13:55 2024

@author: elass
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

# Input data
Density = [1800, 1712, 1800, 1830, 1643, 1920] #kg/m^3
E_Modulus = [30.9, 54.5, 39.065, 37.97, 27.97, 15.32] #GPa
Density_Actual = [3000] #kg/m^3 --> CHANGE
E_ModActual = [50] #GPa --> CHANGE

# Combine the data into an array of points
points = np.column_stack((Density, E_Modulus))

# Function to draw an ellipse around points
def draw_ellipse_around_points(points):
    # Calculate the mean of the points
    center = np.mean(points, axis=0)
    
    # Calculate the covariance matrix and its eigenvalues and eigenvectors
    cov = np.cov(points, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    
    # Width and height of the ellipse are sqrt of eigenvalues (standard deviations)
    # multiplied by a factor for scaling (to ensure the ellipse covers all points)
    width, height = 2.1 * np.sqrt(eigenvalues) * 2.1  
    
    # Calculate the angle of rotation in degrees
    angle = np.arctan2(*eigenvectors[:,0][::-1])
    angle = np.degrees(angle)
    
    # Create an ellipse
    ellipse = Ellipse(xy=center, width=width, height=height, angle=angle, 
                      edgecolor='blue', fc='lightblue', alpha=0.5, lw=2)
    
    return ellipse

# Draw the ellipse
ellipse = draw_ellipse_around_points(points)

# Plotting
fig, ax = plt.subplots()
ax.scatter(Density, E_Modulus, color='black', label='Literature Values')
ax.add_patch(ellipse)
plt.scatter(Density_Actual, E_ModActual, color = 'red', label = 'Actual Value')
ax.set_xlabel('Density (kg/m^3)')
ax.set_ylabel('Elastic Modulus (GPa)')
ax.set_title('Ashby Plot: Elastic Modulus vs. Density')
ax.legend(loc='lower right')
plt.grid(True)
ax.set_aspect('auto', 'datalim')
plt.show()
