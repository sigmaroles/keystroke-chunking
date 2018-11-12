import numpy as np
import re
#digraph_list = ('th', 'he', 'an', 'in', 're', 'er', 'on', 'at', 'nd', 'to', 'ou', 'es', 'se', 'ng', 'be', 'nt')

chars_alp = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
chars_spl = ('.', ',', ' ', '?', '-', '\'', ';')
chars_num = ('0','1','2','3','4','5','6','7','8','9')
chars_command = (' ', ' ', ' ', ' ', ' ', ' ')
chars_arrow = (' ', ' ', ' ', ' ')

codes_spl = (190,188,32,191,189,222,186)
codes_alp = tuple(range(65,91))
codes_num = tuple(range(48,58))
codes_arrow = (37,38,39,40)
codes_command = (16,17,18,8,46,13)

allchars = chars_alp+chars_spl+chars_num+chars_command+chars_arrow
allcodes = codes_alp+codes_spl+codes_num+codes_command+codes_arrow

# forward map, aka convert keycode to alphabet
fmap = dict(list(zip(allcodes, allchars)))
# convert alphabet to keycode, because why not
revmap = dict(list(zip(allchars, allcodes)))

digraph_list = tuple([x + ' ' for x in chars_alp] + [' ' + x for x in chars_alp])

def code2chr(ck):
    try:
        ret = fmap[ck]
    except KeyError:
        ret = ' '
    return ret

# wrapper function for discovering the digraph kcode values
# never pass capitalized letters, they will be silently ignored
def digr2code(digr):
    ret = []
    for ch in digr:
        ret.append(chr2code(ch))
    return tuple(ret)

def chr2code(ch):
    try:
        ret = revmap[ch.lower()]
    except KeyError:
        ret = ''
    return ret
        
def count_digr_freq(txt):
    txt = txt.lower()
    dcounts = np.zeros(len(digraph_list), dtype='int32')
    for tindx, ch in enumerate(txt):
        try:
            pair = txt[tindx] + txt[tindx+1]
        except IndexError:
            pass
        for dindx, digr in enumerate(digraph_list):
            if pair == digr:
                dcounts[dindx] += 1
                
    return dcounts
    
    
# argument: list of lists, of unequal length
# returns: tuple, first element is the longest list, second element is list of the other lists
# note: if two longest lists, first one is considered to be longest
def splitlist(data):
    argmaxlen = np.argmax([len(x) for x in data])
    othlist = [_f for _f in [data[indx] if (not indx==argmaxlen) else None for indx in range(len(data))] if _f]
    return data[argmaxlen], othlist