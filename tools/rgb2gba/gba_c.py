
def get_img_header(filename:str, tileset_n_tiles:int, map_n_tiles:int, palette_n_colors:int) -> str:
    '''Recibe datos sobre el header para devolver un str con el texto del header (fichero\.h).'''
    out_str = ''
    str_list = list()

    nl = '\n'
    e = ' '
    str_list.append(str('#ifndef' +e+ filename.upper() + '_H' + nl))
    str_list.append(str('#define' +e+ filename.upper() + '_H' + nl))
    str_list.append(nl)
    str_list.append(str('#define' +e+ filename+'_tiles_len'+str(tileset_n_tiles*64) + nl))
    str_list.append(str('extern const unsigned short' +e+ filename+'_tiles'
        +'['+str(tileset_n_tiles*32)+']' +e+ '__attribute__((aligned(4)))' + ';' + nl))
    str_list.append(nl)
    str_list.append(str('#define' +e+ filename+'_map_len'+str(map_n_tiles*2) + nl))
    str_list.append(str('extern const unsigned short' +e+ filename+'_map'
        +'['+str(map_n_tiles)+']' +e+ '__attribute__((aligned(4)))' + ';' + nl))
    str_list.append(nl)
    str_list.append(str('#define' +e+ filename+'_pal_len' + str(palette_n_colors*2) + nl))
    str_list.append(str('extern const unsigned short' +e+ filename+'_pal'
        +'['+str(palette_n_colors*2)+']' +e+ '__attribute__((aligned(4)))' + ';' + nl))
    str_list.append(nl)
    str_list.append(str('#endif' + nl))

    return ''.join(str_list)

def get_img_source(filename:str, tileset_dic : dict, tileset_n_tiles:int, map, map_n_tiles:int, palette, palette_n_colors:int, color_list) -> str:
    str_list = list()
    e = ' '
    nl = '\n'
    coma = ','
    str_list.append(str('const unsigned short' +e+ filename+'_tiles'+'['+str(tileset_n_tiles*32)+']' 
        +e+ '__attribute__((aligned(4)))' +e+ '=' +e+ '{'+nl))

    values = tileset_dic.values()
    for tile_info in values:
        str_list.append('/* tile '+e+ str(tile_info[0])+nl)
        str_list.append(str(tile_info[1])+nl)
        str_list.append('*/'+nl)
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
                    str_list.append('0x{:02x}'.format(pixel)+p1+',')
            str_list.append(nl)
        str_list.append(nl)
    str_list.append('};'+nl)

    str_list.append('const unsigned short' +e+ filename+'_pal'+'['+str(palette_n_colors)+']' 
        +e+ '__attribute__((aligned(4)))' +e+ '=' +e+ '{'+nl)

    entries = 0
    max_entries_per_line = 8
    for color in color_list:
        if entries == 0:
            str_list.append('\t')
        str_list.append(color + coma)
        
        # formatea 8 colores por linea
        entries += 1
        if entries >= max_entries_per_line:
            str_list.append(nl)
            entries = 0
    str_list.append(nl)
    str_list.append('};'+nl)


    str_list.append('const unsigned short' +e+ filename+'_map'+'['+str(map_n_tiles)+']' 
        +e+ '__attribute__((aligned(4)))' +e+ '=' +e+ '{'+nl)

    entries = 0
    max_entries_per_line = 8
    for tile_i in map:
        if entries == 0:
            str_list.append('\t')
        map_entry = '0x{:04x}'.format(tile_i)
        str_list.append(map_entry + coma)
        
        # formatea 8 colores por linea
        entries += 1
        if entries >= max_entries_per_line:
            str_list.append(nl)
            entries = 0

    str_list.append('};'+nl)

    return ''.join(str_list)