import enum
import os
import sys
from sys import stdin
from PIL import ImageColor

def clear():
    os.system('clear')

def rgb15(r, g, b) -> str:
    '''Convert (r,g,b) to 15 bits hexadecimal string for GBA palette purposes.
    
    Receives r, g, b ints (preferably 16 bits) as arguments and returns a 16 bit hexacedimal (0x0000).
    Suited for the GBA palette graphics RAM.'''
    #return hex(((r >> 3) & 31) | (((g >> 3) & 31) << 5) | (((b >> 3) & 31) << 10)  )
    hex15 = ((r >> 3) & 31) | (((g >> 3) & 31) << 5) | (((b >> 3) & 31) << 10)
    return "0x{:04x}".format(hex15)

def read_file():
    with open(sys.argv[1]) as f:
        for line in f:
            print(line, end='')
        print()

def read_arguments():
    import sys
    for arg in sys.argv[1:]:
        rgb_int_tuple = tuple(int(arg[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = rgb_int_tuple
        print(rgb15(r, g, b))

def parse(f, n_colors, int_tuples) -> int:
    '''Parses the file f line by line, getting each rgb value from hex to int, to finally store it in int_tuples; returns n_colors so it's not lost.'''
    for line in f:
        n_colors += 1
        int_tuples.append(tuple(int(line[i:i+2], 16) for i in (0, 2, 4)))
    return n_colors

def print_c_format(n_colors, int_tuples) -> int:
    '''Prints the values contained in int_tuples in C source, including the variables; returns n_colors so it's not lost.'''
    print('#define brinPalLen', n_colors*2)
    print('const unsigned short brinPal[', n_colors, '] = {')
    coma = ','
    entries = 0
    max_entries_per_line = 8
    for tupla in int_tuples:
        # imprime hex
        r, g, b = tupla
        if entries == 0:
            print('\t', end='')
        print(rgb15(r, g, b) + coma, end='')
        
        # formatea 8 colores por linea
        entries += 1
        if entries >= max_entries_per_line:
            print('')
            entries = 0
    print()
    print('};')
    return n_colors

def print_hex_format(n_colors, int_tuples) -> int:
    '''Prints the values contained in int_tuples as 0xFFFF, one each line; returns n_colors so it's not lost.'''
    for tupla in int_tuples:
        # imprime hex
        r, g, b = tupla
        print(rgb15(r, g, b))
    return n_colors

class OutputFormat(enum.Enum):
    C = 1
    HEX0x = 2

if __name__ == '__main__':
    #print('rgb2gba', sys.argv)
    # variables
    n_colors = 0
    int_tuples = list()
    print_format = OutputFormat.C

    # arguments parsing. rgb2gba.py -OUTPUT_OPTION [INFILE]
    infile = ''
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "-c":
            print_format = OutputFormat.C
        elif sys.argv[1] == "-hex":
            print_format = OutputFormat.HEX0x
    
    if len(sys.argv) > 2:
        infile = sys.argv[2]

    
    input = ''
    if infile:
        input = infile
    else:
        input = sys.stdin

    # lee el primer fichero pasado por argumentos (en argv[2])
    # si no hay infile, lo lee de stdin
    if input == infile:
        with open(input) as f:
            n_colors = parse(f, n_colors, int_tuples)
    else:
        n_colors = parse(stdin, n_colors, int_tuples)
    
    # muestra en stdout
    if print_format == OutputFormat.C:
        n_colors = print_c_format(n_colors, int_tuples)
    elif print_format == OutputFormat.HEX0x:
        n_colors = print_hex_format(n_colors, int_tuples)
