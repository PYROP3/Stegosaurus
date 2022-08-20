import argparse
import imageio
import sys

from common import create_dictionary, err

parser = argparse.ArgumentParser(description='Encode data into steganography images')
parser.add_argument('source', type=str,
                    help='The image containing steganography data to be decoded')
parser.add_argument('destination', type=argparse.FileType('w', encoding='utf-8'), nargs='?', default=sys.stdout,
                    help='The name of the created file with the extracted data. If ommited, will write to stdout')
parser.add_argument('--channels', type=str, default='rgba',
                    help='The ordered list channels to use. Using more channels allows for more data to be stored')
parser.add_argument('--bits', type=int, default=2, choices=range(1, 9),
                    help='Usable bit length. Bigger lengths allow for more data to be encoded, but also make the artifacts more noticeable')
parser.add_argument('--verbose', action='store_true',
                    help='Write more output. This will be ignored if destination is not present.')

args = parser.parse_args()

is_verbose = args.verbose and args.destination != sys.stdout

original_img = imageio.v2.imread(args.source)
out_file = args.destination

channel_data = args.channels
usable_bit_length = args.bits
    
finished = False
cx = 0
cy = 0
channel_dictionary = {'r':0,'g':1,'b':2,'a':3}
binary_dictionary = create_dictionary(0, 2**usable_bit_length)

current_channel_position = 0
outmsg = ''
current_char_binary = ''
while not finished:
    while len(current_char_binary) < 8:
        try:
            cc = channel_dictionary[channel_data[current_channel_position]]
        except KeyError:
            err('Error: Unrecognized channel ' + channel_data[current_channel_position])

        batch = original_img[cx,cy,cc] % (2**usable_bit_length)
        if is_verbose: print('Batch is ' + str(batch))
        current_char_binary += binary_dictionary[batch]
        cx += 1
        if cx >= original_img.shape[0]:
            cx = 0
            cy += 1
            if cy >= original_img.shape[1]:
                cy = 0
                current_channel_position += 1
                if current_channel_position > 3:
                    err('Something went wrong!')
    
    if is_verbose: print('Got binary >= 8 as ' + current_char_binary)
    char_int = int(current_char_binary[:8], 2)
    this_char = chr(char_int)
    if is_verbose: print('B:' + str(current_char_binary[:8]) + ' - C:' + this_char)
    if this_char == '\0':
        finished = True
    else:
        outmsg += this_char
        current_char_binary = current_char_binary[8:]

if is_verbose: print('Writing output...')
out_file.write(outmsg)
out_file.close()