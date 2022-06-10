import sys
import os

import pprint
from PIL import Image
import numpy as np
import scale_down
import rgb2gba
import subprocess

def parse_infile_palette(infile_palette):
    pass

def subprocess_palette(img_in_colors):
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
            palette_dic[gba_color] = i
            i = i + 1

def ressample(arr, N):
    '''Resizes arr as a list of tiles of NxN size'''
    A = []
    for v in np.vsplit(arr, arr.shape[0] // N):
        A.extend([*np.hsplit(v, arr.shape[0] // N)])
    return np.array(A)

def print_img_header(filename:str, tileset_n_tiles:int, map_n_tiles:int, palette_n_colors:int):
    '''Prints the header file for a background converted with this tool.'''
    #print('#ifndef', filename.upper()+'_H')
    #print('#define', filename.upper()+'_H')

    print('#define', filename+'_tiles_len', tileset_n_tiles*64)
    #print('extern const unsigned short', filename+'_tiles'+'['+str(tileset_n_tiles*32)+']', '__attribute__((aligned(4)))', ';')
    
    print('#define', filename+'_map_len', map_n_tiles*2)
    #print('extern const unsigned short', filename+'_map'+'['+str(map_n_tiles)+']', '__attribute__((aligned(4)))', ';')

    print('#define', filename+'_pal_len', palette_n_colors*2)
    #print('extern const unsigned short', filename+'_pal'+'['+str(palette_n_colors*2)+']', '__attribute__((aligned(4)))', ';')
    
    #print('#endif')

def print_img_source(filename:str, tileset, tileset_n_tiles:int, map, map_n_tiles:int, palette, palette_n_colors:int, color_list):
    print('const unsigned short', filename+'_tiles'+'['+str(tileset_n_tiles*32)+']', '__attribute__((aligned(4)))', '=', '{')

    data = ''
    values = tile_dic.values()
    for tile_info in values:
        print('//tile', tile_info[0])
        print('/*')
        print(tile_info[1])
        print('*/')
        for row in tile_info[1]:
            cont = 0
            p1 = 0
            for pixel in row:
                # los escribe invertidos por lios de la gba
                if cont == 0:
                    cont=1
                    p1 = '{:02x}'.format(pixel)
                else:
                    cont=0
                    print('0x{:02x}'.format(pixel)+p1, end=',')
            print('')
        print('')
    print(data)

    print('};')

    print('const unsigned short', filename+'_pal'+'['+str(palette_n_colors)+']', '__attribute__((aligned(4)))', '=', '{')
    coma = ','
    entries = 0
    max_entries_per_line = 8
    for color in color_list:
        if entries == 0:
            print('\t', end='')
        print(color + coma, end='')
        
        # formatea 8 colores por linea
        entries += 1
        if entries >= max_entries_per_line:
            print('')
            entries = 0
    print()
    print('};')


    print('const unsigned short', filename+'_map'+'['+str(map_n_tiles)+']', '__attribute__((aligned(4)))', '=', '{')
    coma = ','
    entries = 0
    max_entries_per_line = 8
    for tile_i in map:
        if entries == 0:
            print('\t', end='')
        map_entry = '0x{:04x}'.format(tile_i)
        print(map_entry + coma, end='')
        
        # formatea 8 colores por linea
        entries += 1
        if entries >= max_entries_per_line:
            print('')
            entries = 0

    print('};')

    


if __name__ == '__main__':
    #+-------------------------------------------------+
    #|   1. LEER ARGV                                  |
    #+-------------------------------------------------+
    # coge imagen por el primer argumento (argv1)
    img_infile = sys.argv[1]
    img_in_filename, img_in_extension = os.path.splitext(img_infile)

    #--------------------------------------------------+
    #|   2. DETECTAR SI SE INTRODUJO O NO UNA PALETA   |
    #+-------------------------------------------------+
        ### 2.1 TODO TRATAR CADA CASO

    # generamos nombre para el fichero .c q contendrá la imagen
    f, e = os.path.splitext(img_infile)
    img_outfile = f + "_gba" + ".c"
    
    #+-------------------------------------------------+
    #|  3. PASAR IMG A GBA                             |
    #+-------------------------------------------------+
    #| 3.1 guarda imagen data |
    img_in = Image.open(img_infile)
    palette_dic = dict()
    #color_list = list()
    color_list_gba = list()
    
    #| 3.2 recoge paleta de fichero dado parseandolo |#
    i : int = 0
    with open('paleta_resurrect_64.txt') as f:
        for color in f:
            color = color.strip('\n')
            color_list_gba.append(color)
            palette_dic[color] = i
            i = i + 1

    #print('color_list_gba\n',color_list_gba)
    #print('palette_dic\n', palette_dic)

    #| 3.3 pasa rgb de imagen a indices en la paleta |
    img_in_data = np.array(img_in, dtype=np.int8)
    error_log = ''
    #print('size', img_in_data.size)
    #print('dimensions size', img_in_data.shape)

    img_out_gba = np.empty(img_in_data.shape[0:2], dtype=np.int8)
    #print('img_out_gba info', img_out_gba.size, img_out_gba.shape)
    for y in range(img_in_data.shape[1]):
        for x in range(img_in_data.shape[0]):
            r, g, b, a = img_in_data[x][y] # descartamos el tercer valor q es alpha
            gba_color = rgb2gba.rgb15(r, g, b)
            if gba_color in color_list_gba:
                img_out_gba[x,y] = palette_dic[gba_color]
            else:
                # si no existe el color en la paleta por ahora lo pone transparente
                img_out_gba[x,y] = palette_dic['0x7fff']
                error_log += str('error con color'+gba_color+', es distinto a colores en paleta\n')

    #print (error_log)
    #print (img_out_gba)


    #+-------------------------------------------------+
    #|  4. TILING                                      |
    #+-------------------------------------------------+
    #| 4.1 crea lista 2D para manejar mejor las tiles |
    # primero necesitamos formatear o coger bien los datos
    tile_dic = dict() # tileset en un diccionario, key=str(tile_matrix), value=(i, tile_matrix)
    #tile_set = set() # tileset, tiles saved as np.ndarray
    palette = list()

    #| 4.2 crea la lista de tiles a partir de la lista 2D |
    # tiles es una lista de np.NDArray 
    img_tiles = ressample(img_out_gba, 8)

    #| 4.3 Crea diccionario de tiles para tener el tileset guardado |
    i = 0
    i_dic = 0
    for tile in img_tiles:
        tile_s = str(tile)
        #print('# tile', i, '#\n', tile_s)
        i += 1
        if tile_s not in tile_dic:
            tile_dic[tile_s] = (i_dic, tile)
            #tile_set.add(tile)
            i_dic += 1
    
    #print(tiles_dic)
    #for tile in img_tiles:
    #    print(str(tile) == str(img_tiles[0]))

    #+-------------------------------------------------+
    #|  5. TILEMAP                                     |
    #+-------------------------------------------------+
    #| 5.1 pasamos lista de tiles a lista de indices   |
    tile_map = list() # map of the image as tile indexes
    for tile in img_tiles:
        tile_s = str(tile)
        tile_index = tile_dic[tile_s][0]
        tile_map.append(tile_index)
    #print(tile_map)
    
    #+-------------------------------------------------+
    #|  5. GENERAR FICHEROS                            |
    #+-------------------------------------------------+
    #| 5.1 TODO rutas de ficheros etc |
    filename = img_in_filename
    outfile_h = filename+".h"
    outfile_c = filename+".c"

    #| 5.2 generar fichero y escribir |
    with open(outfile_h, 'a') as f_h:
        try:
            print_img_header(filename, len(tile_dic), len(img_tiles), 256)
            print()
            print_img_source(filename, tile_dic, len(tile_dic), tile_map, len(img_tiles), palette, 256, color_list_gba)
            #item = tile_dic.popitem()
            #print(item[1][1])
            #print(item[1][1][0][0])
            #print(type(item[1][1][0][0]))
            f_h.close()
        except OSError as error:
            print(error)
