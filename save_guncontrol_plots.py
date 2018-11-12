
#from parse_kd import *
import re
import pandas as pd
from chunk_utils import *
import matplotlib
import matplotlib.pyplot as plt
data_dir = './data/dw_freetext/'

matplotlib.rcParams['figure.figsize'] = 15,22


df = pd.read_csv(data_dir+'GunControl_400.csv', delimiter='\t')
df_filtered = df[df['Task']=='Copy_2']
# "Copy_2" column = when they're stating true opinion, repeating (transcribing) the essay already written

"""
texts = df_filtered['ReviewText']
with open(data_dir+'_allTexts_guncontrol.txt', 'w') as fh:
    for text in texts:
        fh.write(text)
        fh.write('\n\n========================================================\n\n')
"""

phrases = ["criminal", "constitution", "amendment", "fundamental", "right", "gun", "control", "safe", "citizen", 
           "kill", "violence", "strongly", "think", "feel", "believe", "law", "police", "support", "people", "country",
           "weapon", "understand", "militia", "careful", "rifle", "firearm", "American"
           ]

# df_filtered.shape[0]
for textIndex in range(200):
    rawkd = df_filtered['ReviewMeta'].iloc[textIndex]
    uid = df_filtered['UserName'].iloc[textIndex]
   
    ypos = 0.01
    ydelta = 0.0157
    print ("User:"+uid+ " -- " + str(textIndex))

    for phrase in phrases:
        phrase_keys = get_phrases_from_rawkd(rawkd, phrase)    
        worddelays = [keypress2delays(phrase, keys) for keys in phrase_keys]

        if len(worddelays):
            #print ("word {} typed {} times".format(phrase,len(worddelays)))
            for dd in worddelays:
                xposvector = get_xpos_from_delays(dd, space_min = 0.007, max_delta_spacing=0.04)
                for char, xpos in zip(phrase, xposvector):
                    plt.text(xpos, ypos + ydelta, char, fontsize=20)
                ypos += ydelta

    fname = ".//images//dw_freetext//plots_{}_.svg".format(uid)
    plt.title("user : " + uid, fontsize=34)
    plt.tight_layout()
    plt.savefig(fname, format='svg')
    plt.close()    