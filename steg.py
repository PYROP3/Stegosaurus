import numpy as np
import math
from PIL import Image, ImageDraw
import imageio
import sys
import re

import argvParser as parser

def textToBinary(source):
    #if isVerbose: print('Got source ' + source)
    out = ''
    for char in source:
        #if isVerbose: print('Analizing char ' + char)
        #out += str(bin(int(char.encode('hex'), 16)))[2:].zfill(8)
        out += str(bin(ord(char)))[2:].zfill(8)
    return out + '0'*8
    #return bin(int(source.encode('hex'), 16))[2:].zfill(8*len(source))
    
def createDictionary(binToInt, length):
    dic = {}
    pad = int(math.ceil(math.log(length,2)))
    if binToInt:
        for i in range(length):
            dic[str(bin(i)[2:].zfill(pad))] = i
        if isVerbose: print('Created dictionary ' + repr(dic))
        return dic
    else:
        for i in range(length):
            dic[i] = str(bin(i)[2:].zfill(pad))
        if isVerbose: print('Created dictionary ' + repr(dic))
        return dic

isVerbose = parser.exists(sys.argv, '--verbose') or parser.exists(sys.argv, '-v')
will_decode = parser.exists(sys.argv, '--decode') or parser.exists(sys.argv, '-d')

usable_bit_length = int(parser.getNextValue(sys.argv, '-b', 2))

if usable_bit_length < 1:
    print('Warning: Bit length chosen is too small (min=1), increasing to 2')
    usable_bit_length = 2

if usable_bit_length > 8:
    print('Warning: Bit length chosen is too big (max=8), reducing to 2')
    usable_bit_length = 2

channel_data = parser.getNextValue(sys.argv, '-c', None)
if channel_data == None:
    print('Error: Please input which channels to modify (-c)')
    exit()

image_path = parser.getNextValue(sys.argv, '-s', None)

if image_path == None:
    print('Error: Please input a source image (-s)')
    exit()
    
try:
    original_img = imageio.imread(image_path)
except OSError:
    print('Error: image @ ' + image_path + ' not found!') 
    exit()

original_filetype = re.search(r'\..+',image_path).group()
print('Image found!')



if not will_decode:
    file_path = parser.getNextValue(sys.argv, '-f', None)

    if file_path == None:
        print('Error: Please input a source file (-f)')
        exit()
        
    try:
        original_file = open(file_path, 'r')
    except IOError:
        print('Error: file @ ' + file_path + ' not found!')
        exit()
       
    out_image_path = parser.getNextValue(sys.argv, '-o', None)

    if out_image_path == None:
        print('Error: Please input a name for the output image (-o)')
        exit()
        
        
    bits = textToBinary(original_file.read())
    original_file.close()
    if isVerbose: print('Translated text!')
    if len(bits)/2 > (original_img.shape[0] * original_img.shape[1] * len(channel_data)):
        print('Error: image too small for intended file! Use more channels or get a bigger image.')
        exit()

    cx = 0
    cy = 0
    channel_dictionary = {'r':0,'g':1,'b':2,'a':3}
    #binary_dictionary  = {'00':0,'01':1,'10':2,'11':3}
    binary_dictionary = createDictionary(1, 2**usable_bit_length)
    current_channel_position = 0

    original_length = float(len(bits))
    while len(bits):
        batch = bits[:usable_bit_length]
        bits = bits[usable_bit_length:]
        try:
            cc = channel_dictionary[channel_data[current_channel_position]]
        except KeyError:
            print('Error: Unrecognized channel ' + channel_data[current_channel_position])
            exit()
        
        current_pixel = original_img[cx,cy,cc] 
        original_img[cx,cy,cc] = current_pixel - current_pixel % (2**usable_bit_length) + binary_dictionary[batch]
        if isVerbose: print('Pixel ' + str(cx) + ',' + str(cy) + ': ' + str(current_pixel) + ' => ' + str(original_img[cx,cy,cc]))
        cx += 1
        if cx >= original_img.shape[0]:
            cx = 0
            cy += 1
            if cy >= original_img.shape[1]:
                cy = 0
                current_channel_position += 1
                if current_channel_position > 3:
                    print('Something went wrong!')
                    exit()
        if isVerbose: print(str((1.0 - len(bits) / original_length) * 100.0) + '%')
    
    print('Finished encoding!')
    if re.search(r'\..+',out_image_path) == None:
        out_image_path += original_filetype
    imageio.imwrite(out_image_path, original_img)
    print('Finished writing image to file!')
    if isVerbose: print('Top left corner is ' + repr(original_img[0,0,0]))
else:
    file_path = parser.getNextValue(sys.argv, '-f', None)
    if file_path == None:
        print('Error: Please input a destination file (-f), will create one if not found, and will overwrite one if found')
        
    finished = 0
    cx = 0
    cy = 0
    channel_dictionary = {'r':0,'g':1,'b':2,'a':3}
    #binary_dictionary  = {0:'00',1:'01',2:'10',3:'11'}
    binary_dictionary = createDictionary(0, 2**usable_bit_length)
    current_channel_position = 0
    outmsg = ''
    current_char_binary = ''
    while not finished:
        #current_char_binary = ''
        while len(current_char_binary) < 8:
        #for position_in_char in range(8/(2**usable_bit_length)): #BREAKS WHEN NOT A POWER OF 2
            try:
                cc = channel_dictionary[channel_data[current_channel_position]]
            except KeyError:
                print('Error: Unrecognized channel ' + channel_data[current_channel_position])
                exit()
            batch = original_img[cx,cy,cc] % (2**usable_bit_length)
            if isVerbose: print('Batch is ' + str(batch))
            current_char_binary += binary_dictionary[batch]
            cx += 1
            if cx >= original_img.shape[0]:
                cx = 0
                cy += 1
                if cy >= original_img.shape[1]:
                    cy = 0
                    current_channel_position += 1
                    if current_channel_position > 3:
                        print('Something went wrong!')
                        exit()
        #if len(current_char_binary) != 8:
        #    print('Something went wrong!')
        #    exit()
        
        if isVerbose: print('Got binary >= 8 as ' + current_char_binary)
        #char_int = int('0b' + current_char_binary[8:], 2)
        char_int = int(current_char_binary[:8], 2)
        this_char = chr(char_int)
        if isVerbose: print('B:' + str(current_char_binary[:8]) + ' - C:' + this_char)
        if this_char == '\0':
            finished = 1
        else:
            outmsg += this_char
            current_char_binary = current_char_binary[8:]
    out_file = open(file_path, 'w')
    out_file.write(outmsg)
    out_file.close()
    #print(outmsg)
