import numpy as np
from PIL import Image

if __name__ == '__main__':
    img = Image.open('pueblo16_scaled_down.png')
    img_np = np.array(img)

    print(img_np[0])

    print(img_np[0][1][0:3])
    r, g, b, c = img_np[0][1]
    print(r, g, b, c)

    for row in img_np:
        for color in img_np:
            print(color)