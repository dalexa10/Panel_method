import matplotlib.pyplot as plt
import numpy as np

#Plotting format

def af_plot(x, y):
    width = 10
    plt.figure(figsize=(width, width))
    plt.grid()
    plt.xlabel('x', fontsize=16)
    plt.ylabel('y', fontsize=16)
    plt.plot(x, y, color='k', linestyle='-', linewidth=2)
    plt.axis('scaled')
    plt.xlim(-0.1, 1.1)
    plt.ylim(-0.1, 0.1)
    return

def panel_plot(x,y, panels):
    # plot the geometry and the panels
    width = 10
    plt.figure(figsize=(width, width))
    plt.grid()
    plt.xlabel('x', fontsize=16)
    plt.ylabel('y', fontsize=16)
    plt.plot(x, y, color='k', linestyle='-', linewidth=2)
    plt.plot(np.append([panel.xa for panel in panels], panels[0].xa),
                np.append([panel.ya for panel in panels], panels[0].ya),
                linestyle='-', linewidth=1, marker='o', markersize=6, color='#CD2305')
    Xc = [panel.xc for panel in panels]
    Yc = [panel.yc for panel in panels]
    Betta = [panel.beta for panel in panels]
    plen = [panel.len for panel in panels]
    print(np.array(Betta)*180/np.pi)
    Xn = np.zeros(2)
    Yn = np.zeros(2)
    for i in range(len(Xc)):
        Xn[0] = Xc[i]
        Yn[0] = Yc[i]
        if Yc[i] >= 0:
            Yn[1] = Yc[i] + plen[i] * np.sin(Betta[i])
            Xn[1] = Xc[i] + plen[i] * np.cos(Betta[i])
        else:
            Yn[1] = Yc[i] + plen[i] * np.sin(Betta[i]+np.pi)
            Xn[1] = Xc[i] + plen[i] * np.cos(Betta[i]+np.pi)
        if i == 0:  # For first panel
            plt.plot(Xn, Yn, 'b-', label='First Panel')  # Plot the first panel normal vector
        elif i == 1:  # For second panel
            plt.plot(Xn, Yn, 'g-', label='Second Panel')  # Plot the second panel normal vector
        else:  # For every other panel
            plt.plot(Xn, Yn, 'k-')

    plt.axis('scaled')
    plt.xlim(-0.1, 1.1)
    plt.ylim(-0.1, 0.1)
    return