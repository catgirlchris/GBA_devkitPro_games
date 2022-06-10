import sys
import os
from PIL import Image

import reprlib
import pprint

def thumbnail(infile, outfile_name, extension='.png', size=(128,128)):
    outfile = outfile_name+extension
    try:
        with Image.open(infile) as img:
            img.thumbnail(size)
            img.save(outfile)
    except OSError as error:
        print("cannot convert", infile)
        print('error:', error)

def identify_images():
    for infile in sys.argv[1:]:
        try:
            with Image.open(infile) as im:
                print(infile, im.format, f"{im.size}x{im.mode}")
        except OSError:
            pass


if __name__ == '__main__':
    # coge imagen por el primer argumento (argv1)
    infile = sys.argv[1]
    f, e = os.path.splitext(infile)
    outfile = f + "_scaled_down" + ".png"
    

    img_in = Image.open(infile)

    # el tamaño se divide en 16 (4 * 4) pq vamos a recortar 3 de cada 4 pixeles
    recorte = 4
    fill_color = (255, 255, 0)
    img_out_size = (img_in.size[0] // recorte, img_in.size[1] // recorte)
    img_out = Image.new(img_in.mode, img_out_size, fill_color)
    pixel_list = list()

    
    width, height = img_out.size
    img_in_data = img_in.getdata()
    
    # recorre img_in y coge el primer pixel de cada 4, los demas no
    for x in range(0, width*4, 4):
        for y in range(0, height*4, 4):
            img_out.putpixel(xy=(x//4, y//4), value=img_in_data[x+y*width*4])

    try:
        img_out.save(outfile)
    except OSError as error:
        print("cannot convert", infile)
        print(error)
