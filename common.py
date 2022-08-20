import math
import sys

def text_to_binary(source, verbose=False):
    if verbose: print('Got source ' + source)
    out = ''
    for char in source:
        if verbose: print('Analizing char ' + char)
        out += str(bin(ord(char)))[2:].zfill(8)
    return out + '0'*8
    
def create_dictionary(binToInt, length, verbose=False):
    dic = {}
    pad = int(math.ceil(math.log(length,2)))
    if binToInt:
        for i in range(length):
            dic[str(bin(i)[2:].zfill(pad))] = i
        if verbose: print('Created dictionary ' + repr(dic))
        return dic
    else:
        for i in range(length):
            dic[i] = str(bin(i)[2:].zfill(pad))
        if verbose: print('Created dictionary ' + repr(dic))
        return dic

def err(msg: str, code=1):
    print(msg, file=sys.stderr)
    exit(code)