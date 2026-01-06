import numpy as np
import matplotlib.pyplot as plt

def mandlebrot(c, max_iter): 
    z = 0
    
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        
        z = z*z + c

    return max_iter

def mandlebrot_set(xmin, xmax, ymin, ymax, width, height, max_iter):
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    set = np.zeros((height, width))

    for i in range(width):
        for j in range(height):
            c = complex(x[j], y[i])
            set[i, j] = mandlebrot(c, max_iter)

    return set

def getFigure():
    xmin, xmax, ymin, ymax = -2, 1, -1.5, 1.5
    width, height = 2000, 2000
    max_iter = 100

    mandlebrot_image = mandlebrot_set(xmin, xmax, ymin, ymax, width, height, max_iter)

    fig, ax = plt.subplots(figsize=(5,5))
    colored_ax = ax.imshow(mandlebrot_image, extent=[xmin, xmax, ymin, ymax], cmap="hot")
    ax.set_title("Mandlebrot Set Visualization")
    ax.set_xlabel("Real (c)")
    ax.set_ylabel("Imaginary (c)")
    fig.colorbar(colored_ax)

    return fig

