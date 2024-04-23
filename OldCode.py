def test_stiff(strain, stress):
  strain = np.array(strain)
  stress = np.array(stress)
  linear_stress_mask = stress < 6*10**4
  linear_stress = stress[linear_stress_mask]
  linear_strain = strain[linear_stress_mask]
  linear_reg_out = linregress(linear_strain, linear_stress)
  E_mod = linear_reg_out[0]
  plt.plot(linear_strain, linear_stress)
  plt.xlabel('Strain[-]')
  plt.ylabel('Stress[MPa]')
  plt.title('Stress Strain Graph')
  plt.grid(True)
  plt.savefig('Linear' +'.png')
  print(E_mod/10**9)

def stiffness_calc(strain, stress):
  dx_lst=[]
  dy_lst=[]
  lstrain = []
  for i in range(len(strain)):
    if strain[i]<=0.00125:
      lstrain.append(strain[i])
    else:
      break
  for i in range(len(lstrain)-1):
    dx = lstrain[i+1]-lstrain[i]
    dy = (stress[i+1]-stress[i])/dx
    dx_lst.append(dx)
    dy_lst.append(dy)
  dy_lst.append(lstrain[-1]-lstrain[-2])
  bplot_graph(lstrain[15:-1], dy_lst[15:-1], 'Derivatives2')

def calculate_stiffness(strain, stress):
  strain = np.array(strain)
  stress = np.array(stress)
  #strain_stress_funct = interpolate.interp1d(strain, stress, kind = 'cubic' , fill_value='extrapolate')
  stress_derivatives = []
  stress_derivatives.append(stress[1]-stress[0])
  stress_derivatives.append(stress[1]-stress[0])
  for i in range(len(stress)-2):
    k = i+1
    stress_derivatives.append(stress[k+1]-stress[k-1])
  return(stress_derivatives)
  plt.plot(strain, stress_derivatives)
  plt.xlabel('Strain[-]')
  plt.ylabel('Stress[MPa]')
  plt.title('Derivative Stress Strain Graph')
  plt.grid(True)
  
  

  plt.savefig('Derivatives' +'.png')
  
  strain = strain[5:80] #how to fix :(
  stress = stress[5:80]
  stiffnesslist = []

  for i in range(len(stress)):
    stiffnesslist.append(stress[i]/strain[i])

  stiffness = np.average(stiffnesslist)

  return stiffness

def e_mod_plot(E):
  x = []
  y = []
  for i in range(200):
    x.append(strain[i])
    y.append(strain[i]*E)
  bplot_graph(strain, stress, file)


#for i in range(len(stress)):
#  if stress[i]>6*10**4:
#    print((stress[i]/strain[i])/10**6)
#    break
#test_stiff(strain,stress)
#stiffness_calc(strain, stress)
#TESTING DEFINITIONS
#tensile_ultimate = calculate_ult_tens(stress)
#print("Ultimate tensile strength is", tensile_ultimate, "N per meter squared")
#stifness_test = calculate_stiffness(strain, stress)
#print("Stiffness is", stifness_test, "N per m squared")
#toughness = calculate_toughness(strain, stress)
#print("Toughness is", toughness, "N per m squared")

#derivatives = calculate_stiffness(strain, stress)
#max_der = max(derivatives)
#pos_max_der = derivatives.index(max_der)
#max_strain = strain[pos_max_der]
#print(max_der/max_strain)
