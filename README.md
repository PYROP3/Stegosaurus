# Stegosaurus
A steganography script written in Python

## Command structure
The program can be run in either encode or decode mode, and the structure differs a bit. Please refer to the `--help` or `-h` options for information on the arguments.
### Encode
```shell
encode.py [-h] [--channels CHANNELS] [--bits {1,2,3,4,5,6,7,8}] [--verbose] [contents] source destination
```

### Decode
```shell
decode.py [-h] [--channels CHANNELS] [--bits {1,2,3,4,5,6,7,8}] [--verbose] source [destination]
```

## [Steganography](https://en.wikipedia.org/wiki/Steganography)

Steganography is the practice of concealing a message within another message or a physical object. In computing/electronic contexts, a computer file, message, image, or video is concealed within another file, message, image, or video.