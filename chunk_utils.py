"""
Input: a list of raw keystroke data(in string format)
Output: a numpy array, shape (n_iterations, n_characters) 
Assumes the input is correct format (has correct number of keys etc.)
"""

from parse_kd import *
import numpy as np
import re

def kdata2delaysOLD(typedname, rawkd, remove_outliers=False):
    # generate a list of keypress objects from raw strings
    keys = parsekevents(parsekdata(rawkd))
    
    n_chars = len(typedname)
    
    # convert the 1D array to 2D, each element representing one iteration of the typing task
    keys2d = [keys[n_chars*i:n_chars*(i+1)] for i in range(20)]

    # extract the timestamps from the 2D array, other info is irrelevant 
    timestamps = [list(map(lambda y: int(y.avgtime), x)) for x in keys2d]
    
    # extract the delays (flight time after the key was pressed) for each key
    delays = np.array([list(map(lambda x, y: y-x, tstamp, tstamp[1:])) for tstamp in timestamps])
    
    if remove_outliers:
        outlier_thresh = np.std(delays) * 3
        delays[delays>outlier_thresh] = 0
        
"""
Input: a list of raw keystroke data(in string format)
Output: a numpy array, shape (n_iterations, n_characters) 
Assumes the input is correct format (has correct number of keys etc.)
"""

from parse_kd import *
import numpy as np

def kdata2delays(typedname, rawkd):
    # generate a list of keypress objects from raw strings
    keys = parsekevents(parsekdata(rawkd))
    return keypress2delays(typedname, keys)
    

def keypress2delays(typedphrase, keys):
    keys2d = list(zip(keys,keys[1:]))
    timestamps = [list(map(lambda y: int(y.avgtime), x)) for x in keys2d]
    delays = [tst[1]-tst[0] for tst in timestamps]
    return delays


def get_xpos_from_delays(delays, space_min = 0.007, max_delta_spacing = .03, x_begin = 0):
    values = [0] + list(delays) # padding, to indicate "no delay" for first character
    xpos = x_begin
    maxdelay = max(values)
    ret = []
    
    for thisdelay in values:
        # thisdelay is the temporal delay preceeding char that needs to be converted to spatial measure
        space_delta = space_min + ((thisdelay / maxdelay) * max_delta_spacing)
        xpos = xpos + space_delta
        ret.append(xpos)
    
    return ret

def get_phrases_from_rawkd(rawkd, phrase_of_interest):
    keypresses = parsekevents(parsekdata(rawkd))
    txt = ''.join(list(map(lambda x: x.character, keypresses)))
    offset = len(phrase_of_interest)
    indx = [m.start() for m in re.finditer(phrase_of_interest, txt)]
    keys_for_phrase = [keypresses[inn:inn+offset] for inn in indx]
    #print (len(txt), len(keypresses))
    return keys_for_phrase