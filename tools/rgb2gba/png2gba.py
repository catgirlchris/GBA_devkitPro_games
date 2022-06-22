import sys
import os

import pprint
from PIL import Image
import numpy as np
import subprocess
import argparse

import scale_down
import rgb2gba
import gba_c



def subprocess_palette(img_in_colors, color_list, color_list_gba, palette_dict):
    '''Bloque de codigo para llamar a rgb2gba.py y genere paleta a partir de input.'''
    # TODO TEST run subproceso para la paleta
    string = img_in_colors
    process = subprocess.run(['python3', 'rgb2gba.py', '-hex'], 
        text=True, stdout=subprocess.PIPE, input=string)
    output = process.stdout
    #print(process)
    #print('return code:', process.returncode)
    print('### output ###\n', output)

    # parsear paleta
    for line in output.splitlines():
        print(line)
    i = 0
    for tuple in img_in_colors:
        color_frec, color = tuple
        r, g, b = color[0:3] # descartamos el tercer valor q es alpha
        

        gba_color = rgb2gba.rgb15(r, g, b)
        if gba_color not in color_list_gba:
            color_list.append((r, g, b))
            color_list_gba.append(gba_color)
            palette_dict[gba_color] = i
            i = i + 1

def ressample(arr, N):
    '''Resizes arr as a list of tiles of NxN size'''
    A = []
    for v in np.vsplit(arr, arr.shape[0] // N):
        A.extend([*np.hsplit(v, arr.shape[0] // N)])
    return np.array(A)

def clean(infile):
    file_list = list()

    filename, extension = os.path.splitext(infile)
    outfile_h = filename+".h"
    outfile_c = filename+".c"
    
    file_list.append(outfile_c)
    file_list.append(outfile_h)

    print("cleaning...")
    for file in file_list:
        try:
            print("removing", file)
            os.remove(file)
            print("done\n")
        except OSError as error:
            print(error)

def parse_infile_palette(palette_infile, color_list_gba, palette_dic) -> dict:
    '''Parses the given file infile_palette, then adds the colors to the given palette_dic and the color_list'''
    i : int = 0
    with open(palette_infile) as f:
        for color in f:
            color = color.strip('\n')
            color_list_gba.append(color)
            palette_dic[color] = i
            i = i + 1
    return palette_dic

def convert_img_to_palette_index(img_in_data : np.ndarray, img_out_gba : np.ndarray, color_list_gba, palette_dic, error_log):
    '''Converts each pixel in the img_in_data to a color index of the given palette_dic.'''
    for y in range(img_in_data.shape[1]):
        for x in range(img_in_data.shape[0]):
            r, g, b, a = img_in_data[x][y] # descartamos el tercer valor q es alpha
            gba_color = rgb2gba.rgb15(r, g, b)
            
            if gba_color in color_list_gba:
                img_out_gba[x,y] = palette_dic[gba_color]
            else:
                # si no existe el color en la paleta por ahora lo pone transparente
                img_out_gba[x,y] = palette_dic['0x7fff']
                error_log.append('error con color'+str(gba_color)+', es distinto a colores en paleta')

def get_tile_dict(img_tiles : list):
    '''Generates a tileset, saved as a dictionary; adds each unique tile from the given list of tiles (list[np.ndarray])'''
    tile_dict = dict()
    i = 0
    i_dic = 0
    for tile in img_tiles:
        tile_s = str(tile)
        i += 1
        if tile_s not in tile_dict:
            tile_dict[tile_s] = (i_dic, tile)
            i_dic += 1
    return tile_dict

def get_tilemap_from_ndarray(img_tiles : list, tile_dict : dict) -> list():
    '''Returns a tilemap of the given tile_list.'''
    tile_map = list()
    for tile in img_tiles:
        tile_s = str(tile)
        tile_index = tile_dict[tile_s][0]
        tile_map.append(tile_index)
    return tile_map

def create_file(filepath : str, extension : str, text_to_write : str):
    '''Creates a file+extension and writes text_to_write in it; then saves it at the given filepath.'''
    folder, filename = os.path.split(filepath)
    with open(filepath+extension, 'w') as f:
        try:
            print(f'imprimiendo fichero {filepath}{extension}')
            f.write(text_to_write)
            print('terminado')
            f.close()
        except OSError as error:
            print(error)

def convert(img_infile : str, pal_infile : str = '', pal_outfile : str = ''):
    '''Converts the given image_infile to a C format GBA-readable.
    
    pal_infile refers to whether the palette is already given so the color indexing is done using that palette.
    if no pal_file is given it generates a palette from the image.'''
    #+-------------------------------------------------+
    #|  3. PASAR IMG A GBA                             |
    #+-------------------------------------------------+
    #| 3.1 | guarda imagen data |
    img_in = Image.open(img_infile)
    palette_dic = dict()
    color_list_gba = list()

    #|3.2 | prepara matrices pixeles(img_in) y pal_index(img_out)
    img_in_data = np.array(img_in, dtype=np.int8)
    img_out_gba = np.empty(img_in_data.shape[0:2], dtype=np.int8)
    error_log = list()

    #| 3.2 | recoge paleta de fichero dado parseandolo |
    if pal_infile:
        parse_infile_palette(pal_infile, color_list_gba, palette_dic)
    else:
        #TODO get palette from image
        pass

    #| 3.3 | pasa rgb de imagen a indices en la paleta |
    convert_img_to_palette_index(img_in_data, img_out_gba, color_list_gba, palette_dic, error_log)

    #+-------------------------------------------------+
    #|  4. TILING                                      |
    #+-------------------------------------------------+
    #| 4.1 | crea lista 2D para manejar mejor las tiles |
    # primero necesitamos formatear o coger bien los datos
    tile_dict = dict() # tileset en un diccionario, key=str(tile_matrix), value=(i, tile_matrix)
    palette = list()

    #| 4.2 | crea la lista de tiles (np.ndarrays) a partir de la lista 2D |
    img_tiles = ressample(img_out_gba, 8)

    #| 4.3 | Crea diccionario de tiles para tener el tileset guardado |
    tile_dict = get_tile_dict(img_tiles)

    #+-------------------------------------------------+
    #|  5. TILEMAP                                     |
    #+-------------------------------------------------+
    #| 5.1 | pasamos lista de tiles a lista de indices   |
    tile_map = get_tilemap_from_ndarray(img_tiles, tile_dict)
    
    #+-------------------------------------------------+
    #|  5. GENERAR FICHEROS                            |
    #+-------------------------------------------------+
    #| 5.1 | TODO rutas de ficheros etc |
    filepath = img_in_filename
    folder, filename = os.path.split(filepath)

    #| 5.2 | generar fichero y escribir |
    header_str = gba_c.get_img_header(filename, len(tile_dict), len(img_tiles), 256)
    create_file(filepath, '.h', header_str)

    source_str = gba_c.get_img_source(filename, tile_dict, len(tile_dict), tile_map, len(img_tiles), palette, 256, color_list_gba)
    create_file(filepath, '.c', source_str)

#+-------------------------------------------------+
#|  MAIN                                           |
#+-------------------------------------------------+
if __name__ == '__main__':
    #+-------------------------------------------------+
    #|   1. ESTRUCTURA DE LOS ARGUMENTOS               |
    #+-------------------------------------------------+
    parser = argparse.ArgumentParser(description="Converts .png images to a C format readable by the GBA.")
    subparsers = parser.add_subparsers(dest="subparser_name")

    # subparsers
    parser_clean = subparsers.add_parser("clean", help="clean the files generated by the program with the given infile")
    parser_clean.add_argument("infile", help="file that was used with this program. This way the program will erase the files generated by infile.")

    # default parser arguments
    parser_convert = subparsers.add_parser("convert", help="main functionality of the program")
    parser_convert.add_argument("type", choices=['sprite', 'background'],
                                help="type of file (sprite, background) we want to create from the infile")
    parser_convert.add_argument("infile", help="input file")
    parser_convert_palette_group = parser_convert.add_argument_group("palette", "palette commands for input, output and options")
    parser_convert_palette_group.add_argument("-pal_infile", help="file where palette is read from. if no file is given, the program will create a palette from the image infile")
    parser_convert_palette_group.add_argument("-pal_outfile", help="file where palette is written to. if no file is given, STILL TO DECIDE WHAT THE PROGRAM WILL DO")

    # get arguments
    args = parser.parse_args()


    #+-------------------------------------------------+
    #|   2. DETECTAR SI SE INTRODUJO O NO UNA PALETA   |
    #+-------------------------------------------------+
        ### 2.1 | TODO TRATAR CADA CASO

    #+-------------------------------------------------+
    #|   3. LEER ARGS                                  |
    #+-------------------------------------------------+
    # coge imagen por el argumento infile
    img_infile = args.infile
    img_in_filename, img_in_extension = os.path.splitext(img_infile)

    print(args)

    if args.subparser_name == "clean":
        clean(args.infile)
        quit()
    elif args.subparser_name == "convert":
        convert(args.infile, args.pal_infile, args.pal_outfile)

    
    
    
 