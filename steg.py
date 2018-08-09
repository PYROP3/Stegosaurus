import numpy as np
import math
from PIL import Image, ImageDraw
import imageio
import sys
import re

import argvParser as parser

def textToBinary(source):
    out = ''
    for char in source:
        out += str(bin(int(char.encode('hex'), 16)))[2:].zfill(8)
    return out + '0'*8
    #return bin(int(source.encode('hex'), 16))[2:].zfill(8*len(source))

isVerbose = parser.exists(sys.argv, '--verbose') or parser.exists(sys.argv, '-v')
will_decode = parser.exists(sys.argv, '--decode') or parser.exists(sys.argv, '-d')

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
        original_file = open(file_path, 'rb')
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
    binary_dictionary  = {'00':0,'01':1,'10':2,'11':3}
    current_channel_position = 0

    original_length = float(len(bits))
    while len(bits):
        batch = bits[:2]
        bits = bits[2:]
        try:
            cc = channel_dictionary[channel_data[current_channel_position]]
        except KeyError:
            print('Error: Unrecognized channel ' + channel_data[current_channel_position])
            exit()
        
        current_pixel = original_img[cx,cy,cc] 
        original_img[cx,cy,cc] = current_pixel - current_pixel % 4 + binary_dictionary[batch]
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
    
    print('Finished writing!')
    if re.search(r'\..+',out_image_path) == None:
        out_image_path += original_filetype
    imageio.imwrite(out_image_path, original_img)
else:
    file_path = parser.getNextValue(sys.argv, '-f', None)
    if file_path == None:
        print('Error: Please input a destination file (-f), will create one if not found, and will overwrite one if found')
        
    finished = 0
    cx = 0
    cy = 0
    channel_dictionary = {'r':0,'g':1,'b':2,'a':3}
    binary_dictionary  = {0:'00',1:'01',2:'10',3:'11'}
    current_channel_position = 0
    outmsg = ''
    while not finished:
        current_char_binary = ''
        for position_in_char in range(4):
            try:
                cc = channel_dictionary[channel_data[current_channel_position]]
            except KeyError:
                print('Error: Unrecognized channel ' + channel_data[current_channel_position])
                exit()
            batch = original_img[cx,cy,cc] % 4
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
        if len(current_char_binary) != 8:
            print('Something went wrong!')
            exit()
        char_int = int('0b' + current_char_binary, 2)
        this_char = chr(char_int)
        if isVerbose: print('B:' + str(current_char_binary) + ' - C:' + this_char)
        if this_char == '\0':
            finished = 1
        else:
            outmsg += this_char
    out_file = open(file_path, 'w')
    out_file.write(outmsg)
    out_file.close()
    #print(outmsg)
