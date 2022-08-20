import argparse
import imageio
import sys
import os

from common import text_to_binary, create_dictionary, err

parser = argparse.ArgumentParser(description='Encode things into steganography images')
parser.add_argument('contents', type=argparse.FileType('r', encoding='utf-8'), nargs='?', default=sys.stdin,
                    help='The content that will be hidden. If ommited, will read from stdin')
parser.add_argument('source', type=str,
                    help='The image that will be used to hide contents')
parser.add_argument('destination', type=str,
                    help='The name of the generated image')
parser.add_argument('--channels', type=str, default='rgba',
                    help='The ordered list channels to use. Using more channels allows for more data to be stored')
parser.add_argument('--bits', type=int, default=2, choices=range(1, 9),
                    help='Usable bit length. Bigger lengths allow for more data to be encoded, but also make the artifacts more noticeable')
parser.add_argument('--verbose', action='store_true',
                    help='Write more output')

args = parser.parse_args()

is_verbose = args.verbose

original_file = args.contents
original_img = imageio.v2.imread(args.source)
out_image_path = os.fspath(args.destination)

channel_data = args.channels
usable_bit_length = args.bits
    
bits = text_to_binary(original_file.read())
original_file.close()
if is_verbose: print('Translated text!')
if len(bits)/usable_bit_length > (original_img.shape[0] * original_img.shape[1] * len(channel_data)):
    err('Error: image too small for intended file! Use more channels or get a bigger image.')

cx = 0
cy = 0
channel_dictionary = {'r':0,'g':1,'b':2,'a':3}
binary_dictionary = create_dictionary(1, 2**usable_bit_length)
current_channel_position = 0

original_length = float(len(bits))
while len(bits):
    batch = bits[:usable_bit_length].zfill(usable_bit_length)
    bits = bits[usable_bit_length:]
    try:
        cc = channel_dictionary[channel_data[current_channel_position]]
    except KeyError:
        err('Error: Unrecognized channel ' + channel_data[current_channel_position])
    
    current_pixel = original_img[cx,cy,cc] 
    original_img[cx,cy,cc] = current_pixel - current_pixel % (2**usable_bit_length) + binary_dictionary[batch]
    if is_verbose: print('Pixel ' + str(cx) + ',' + str(cy) + ': ' + str(current_pixel) + ' => ' + str(original_img[cx,cy,cc]))
    cx += 1
    if cx >= original_img.shape[0]:
        cx = 0
        cy += 1
        if cy >= original_img.shape[1]:
            cy = 0
            current_channel_position += 1
            if current_channel_position > 3:
                err('Something went wrong!')
    if is_verbose: print(str((1.0 - len(bits) / original_length) * 100.0) + '%')

if is_verbose: print('Finished encoding!')
imageio.imwrite(out_image_path, original_img)
if is_verbose: print('Finished writing image to file!')
if is_verbose: print('Top left corner is ' + repr(original_img[0,0,0]))