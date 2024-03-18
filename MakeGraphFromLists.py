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

def bplot_graph(list1, list2, name):
    if len(list1) != len(list2):
        print("Error: Lists must have the same length.")
        return

    # Create the graph
    plt.plot(list1, list2,'o')
    plt.xlabel('Strain[-]')
    plt.ylabel('Stress[MPa]')
    plt.title('Stress Strain Graph')
    plt.grid(True)
    
    plt.savefig(name+'.png')
