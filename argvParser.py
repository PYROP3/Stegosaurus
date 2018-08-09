def getNextIndex(str, command):
    i = 0
    while i < len(str):
        
        if str[i] == command:
            return i + 1
        i += 1
    return None
    
def getNextValue(str, command, default):
    i = 0
    while i < len(str):
        if str[i] == command and (i + 1) < len(str):
            return str[i + 1]
        i += 1
    return default

def exists(str, command):
    i = 0
    while i < len(str):
        if str[i] == command:
            return 1
        i += 1
    return 0
