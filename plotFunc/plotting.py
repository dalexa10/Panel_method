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
    plt.axis('scaled')
    plt.xlim(-0.1, 1.1)
    plt.ylim(-0.1, 0.1)
    return