import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KernelDensity
from chunk_utils import kdata2delays, get_xpos_from_delays

data_dir = './data/names'
image_dir = './images/'
matplotlib.rcParams['figure.figsize'] = 40,15

datafilenames = list(filter(lambda x: x.endswith('.kdt'), os.listdir(data_dir)))

for fn in datafilenames:

    with open(data_dir+'//'+fn, 'r') as fh:
        filedata = fh.read()
    typedname, rawkd = filedata.split('\n')
    n_chars = len(typedname)
    typedname = typedname.replace(' ', '_')

    delays = np.array(kdata2delays(typedname, rawkd))
    models = [KernelDensity(kernel='gaussian', bandwidth=3.5) for  x in range(delays.shape[1])]
    
    # for each key in the typed word..build a model
    for i in range(delays.shape[1]):
        models[i].fit(delays[:,i].reshape(-1,1))

    generated_delays = []

    for i in range(20):
        generated_iter = [x.sample()[0][0] for x in models]
        generated_delays.append(generated_iter)
        
    generated_delays = np.array(generated_delays)

    ypos = 0.01
    ydelta = 0.0317
    delta_max = 0.036
    delta_min = 0.001

    for dd in generated_delays:
        xposvector = get_xpos_from_delays(dd, space_min = delta_min, max_delta_spacing=delta_max, x_begin=0.51)
        for char, xpos in zip(typedname, xposvector):
            plt.text(xpos, ypos + ydelta, char, fontsize=22, fontweight='bold')
        ypos += ydelta
    plt.text(0.51, ypos+5*ydelta, "Generated vectors (no particular order)", fontsize=34)
        
    ypos = 0.01
    for dd in delays:
        xposvector = get_xpos_from_delays(dd, space_min = delta_min, max_delta_spacing=delta_max, x_begin=0.0)
        for char, xpos in zip(typedname, xposvector):
            plt.text(xpos, ypos + ydelta, char, fontsize=22, fontweight='bold')
        ypos += ydelta
    plt.text(0.0, ypos+5*ydelta, "Typed vectors (bottom row = first iteration)", fontsize=34)


    plt.tight_layout()
    #plt.show()
    svgfname = ".//images//generated_vs_typed_plot_" + typedname + "_.svg"
    plt.savefig(svgfname, format='svg')
    plt.close()
    plt.clf()
    print ("done with ",svgfname)

