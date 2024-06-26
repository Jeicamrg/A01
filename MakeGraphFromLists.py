import matplotlib.pyplot as plt

def plot_graph(list1, list2):
    """
    Plot a graph from two lists.

    Parameters:
    - list1: The first list (x-axis values).
    - list2: The second list (y-axis values).
    """
    # Ensure both lists have the same length
    if len(list1) != len(list2):
        print("Error: Lists must have the same length.")
        return

    # Create the graph
    plt.plot(list1, list2)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Graph')
    plt.grid(True)
    plt.savefig('plot.png')

def bplot_graph(list1, list2, name, ftype):
    if len(list1) != len(list2):
        print("Error: Lists must have the same length.")
        return

    # Create the graph
    plt.plot(list1, list2)
    plt.xlabel('Strain[-]')
    plt.ylabel('Stress[Pa]')
    plt.title('Stress Strain Graph '+(name))
    plt.grid(True)
    
    plt.savefig(ftype + name + '.png')
    plt.clf()

def bplot_graph2(list1, list2, name):
    if len(list1) != len(list2):
        print("Error: Lists must have the same length.")
        return

    # Create the graph
    plt.plot(list1, list2)
    plt.xlabel('Strain[-]')
    plt.ylabel('Stress[Pa]')
    if name[-10]=='\\':
        new_name = name[-9:-4]
    else:
        new_name = name[-10:-4]
    plt.title('Stress Strain Graph '+(new_name))
    plt.grid(True)
    
    plt.savefig(name + '.png')
    plt.clf()
    plt.cla()

