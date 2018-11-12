from util_new import code2chr

class Kevent:
    def __init__(self, data):
        # data[0], data[2] must be convertible to int and long
        self.type = data[1]
        self.tstamp = int(data[0])
        self.kcode = int(data[2])
        self.toignore = False
        
    def __repr(self):
        return "Type:" + self.type + " ; kCode: " + str(self.kcode) +" ; Stamp: " + str(self.tstamp)
    
    # subtract timestamps
    def __sub__(self, other):
        return self.tstamp - other.tstamp
        
    def __add__(self, other):
        return self.tstamp + other.tstamp
        
        
class Keypress:
    def __init__(self, kvtup, kvtdn):
        if not kvtup.kcode == kvtdn.kcode:
            raise ValueError("Bad pair of events to keypress constructor")
        self.press_time = kvtdn.tstamp
        self.release_time = kvtup.tstamp
        self.avgtime = (self.press_time + self.release_time) / 2
        self.kcode = kvtup.kcode
        self.hold_delay = kvtup.tstamp - kvtdn.tstamp
        self.character = code2chr(self.kcode)
    
    def __sub__(self, other):
        # the "average" flight time .. from release events and press events
        return ((self.press_time - other.press_time) + (self.release_time - other.release_time)) / 2

    def __add__(self, other):
        return self.press_time + other.press_time

    def __repr__(self):
        return '[' + self.character + ' ' + str(self.avgtime) + ']'
        
class Digraph:
    def __init__(self, keys):
        # keys should be list, with two Keypress objects
        # keys should be in chronological order
        self.keys = keys
        self.uu = []
        self.dd = []
        for indx in range(len(self.keys)-1):
            self.uu.append(keys[indx+1].rel - keys[indx].rel)
            self.dd.append(keys[indx+1].pre - keys[indx].pre)
        
        
    def __str__(self):
        kcodes = [x.kcode for x in self.keys]
        return str(kcodes)
        
    def getDelays(self):
        holds = [x.delay for x in self.keys]
        return self.dd + self.uu + holds
    
        
# param: list of Kevent objects
# returns: list of Keypress objects
def parsekevents(kevents):
    # aims:
    # 1. construct keypress objects from Kevent objects
    # 2. if repeated keyDowns are detected, take only the first one 
    # for every keydn, go looking for corresponding keyup. may not find one, then discard it.
    # will construct list of keypress objects directly, in one pass
    kpresslist = []
    
    # look at each Kevent...
    for indx, kvt in enumerate(kevents):
        #if kvt.kcode == 8:
        #    continue    # do not mess with backspace
        if kvt.type=='KeyDown' and (not kvt.toignore):
            # go looking for keyup, marking any repeated keydowns as toignore along the way
            for testkvt in kevents[indx+1:]:
                if testkvt.kcode==kvt.kcode:
                    if testkvt.type=='KeyDown':
                        testkvt.toignore=True
                    elif testkvt.type=='KeyUp': # maybe remove this check for performance..
                        # construct a Keypress event!
                        kpresslist.append(Keypress(testkvt, kvt))
                        # since corresponding keyUp was found, break from the inner loop
                        break
                # else nothing to do, carry on
              
    return kpresslist
        
        
    
def parsekdata(row):
    # parsing key events into Kevent objects, in three steps
    # 1. split the entire text into list of key events (separated by semicolon)
    # 2. each event is further separated by space, so split by space
    # 3. finally, remove the mouse events and construct Kevent objects
    # 4. return the list of kevnt objects
    rtokens = [x.split(' ') for x in row.split(';')[:-1]]
    ktokens = [x for x in rtokens if not x[1] == 'MouseUp']
    kevts = [Kevent(x) for x in ktokens]
    return kevts

# take a row of raw events, construct Keypress objects and write corresponding text to a stream
def kvtstream2txt(row, outfile):
    keys = parsekevents(parsekdata(row))
    for key in keys:
        outfile.write(code2chr(key.kcode))

from util_new import code2chr

class Kevent:
    def __init__(self, data):
        # data[0], data[2] must be convertible to int and long
        self.type = data[1]
        self.tstamp = int(data[0])
        self.kcode = int(data[2])
        self.toignore = False
        
    def __repr(self):
        return "Type:" + self.type + " ; kCode: " + str(self.kcode) +" ; Stamp: " + str(self.tstamp)
    
    # subtract timestamps
    def __sub__(self, other):
        return self.tstamp - other.tstamp
        
    def __add__(self, other):
        return self.tstamp + other.tstamp
        
        
class Keypress:
    def __init__(self, kvtup, kvtdn):
        if not kvtup.kcode == kvtdn.kcode:
            raise ValueError("Bad pair of events to keypress constructor")
        self.press_time = kvtdn.tstamp
        self.release_time = kvtup.tstamp
        self.avgtime = (self.press_time + self.release_time) / 2
        self.kcode = kvtup.kcode
        self.hold_delay = kvtup.tstamp - kvtdn.tstamp
        self.character = code2chr(self.kcode)
    
    def __sub__(self, other):
        # the "average" flight time .. from release events and press events
        return ((self.press_time - other.press_time) + (self.release_time - other.release_time)) / 2

    def __add__(self, other):
        return self.press_time + other.press_time

    def __repr__(self):
        return '[' + self.character + ' ' + str(self.avgtime) + ']'
        
class Digraph:
    def __init__(self, keys):
        # keys should be list, with two Keypress objects
        # keys should be in chronological order
        self.keys = keys
        self.uu = []
        self.dd = []
        for indx in range(len(self.keys)-1):
            self.uu.append(keys[indx+1].rel - keys[indx].rel)
            self.dd.append(keys[indx+1].pre - keys[indx].pre)
        
        
    def __str__(self):
        kcodes = [x.kcode for x in self.keys]
        return str(kcodes)
        
    def getDelays(self):
        holds = [x.delay for x in self.keys]
        return self.dd + self.uu + holds
    
        
# param: list of Kevent objects
# returns: list of Keypress objects
def parsekevents(kevents):
    # aims:
    # 1. construct keypress objects from Kevent objects
    # 2. if repeated keyDowns are detected, take only the first one 
    # for every keydn, go looking for corresponding keyup. may not find one, then discard it.
    # will construct list of keypress objects directly, in one pass
    kpresslist = []
    
    # look at each Kevent...
    for indx, kvt in enumerate(kevents):
        #if kvt.kcode == 8:
        #    continue    # do not mess with backspace
        if kvt.type=='KeyDown' and (not kvt.toignore):
            # go looking for keyup, marking any repeated keydowns as toignore along the way
            for testkvt in kevents[indx+1:]:
                if testkvt.kcode==kvt.kcode:
                    if testkvt.type=='KeyDown':
                        testkvt.toignore=True
                    elif testkvt.type=='KeyUp': # maybe remove this check for performance..
                        # construct a Keypress event!
                        kpresslist.append(Keypress(testkvt, kvt))
                        # since corresponding keyUp was found, break from the inner loop
                        break
                # else nothing to do, carry on
              
    return kpresslist
        
        
    
def parsekdata(row):
    # parsing key events into Kevent objects, in three steps
    # 1. split the entire text into list of key events (separated by semicolon)
    # 2. each event is further separated by space, so split by space
    # 3. finally, remove the mouse events and construct Kevent objects
    # 4. return the list of kevnt objects
    rtokens = [x.split(' ') for x in row.split(';')[:-1]]
    ktokens = [x for x in rtokens if not x[1] == 'MouseUp']
    kevts = [Kevent(x) for x in ktokens]
    return kevts

# take a row of raw events, construct Keypress objects and write corresponding text to a stream
def kvtstream2txt(row, outfile):
    keys = parsekevents(parsekdata(row))
    for key in keys:
        outfile.write(code2chr(key.kcode))

if __name__=='__main__':
    print(" some demo goes here ")