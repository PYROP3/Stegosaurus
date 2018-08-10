# Stegosaurus
A steganography script written in Python
## Command structure
The program can be run in either encode or decode mode, and the structure differs a bit. But in both of them, the arguments can be written in any order.
### Encode
```shell
python steg.py -s <image> -f <file> -o <image> -c <channels> [-b <bits>]
```
- `-s <image>`: The image to use as a base;
- `-f <file>`: The file to hide in the image _(still in beta, probably only works with text files)_;
- `-o <image>`: The name of the created image (the extension can be ommitted, and if it is not found, will be the same as the source image);
- `-c <channels>`: The (ordered) list of channels to use. If it fails, try using more channels (r, g, b and a).
- `-b <bits`: Usable bit length (standard value is 2, min=1, max=8). Bigger lengths allow for more data to be encoded, but also makes it more noticeable.

### Decode
```shell
python steg.py -s <image> -f <file> -c <channels> [-b <bits>] --decode
```
- `-s <image>`: The image to decode;
- `-f <file>`: The file to create with the decoded text (will be created if non-existent, will overwrite any existing files);
- `-c <channels>`: The (ordered) list of channels to use. The order has to be the same as when encoded (changing the order can have different results, from simply changing the order of a few big blocks of text, to showing garbled output if the first channels weren't used in the encoding.
- `-b <bits`: Usable bit length (standard value is 2, min=1, max=8). Bigger lengths allow for more data to be encoded, but also makes it more noticeable.
