#include <string.h>
#include <tonc_video.h>
#include <tonc_input.h>

#include <tonc_types.h>

#define vid_mem         ((COLOR*)MEM_VRAM)

#include "img/title_screen.h"





int main() {
	// Configurar el modo de video a modo 3 (bitmap)
    REG_DISPCNT = DCNT_MODE3 | DCNT_BG2;

    // Copiar los datos del fondo al VRAM
    memcpy(vid_mem, title_screen_data, title_screen_width * title_screen_height * 2);


    // Scroll around some
	int x= 0, y= 0;
	while(1)
	{
		vid_vsync();
		key_poll();

		x += key_tri_horz();
		y += key_tri_vert();

		REG_BG0HOFS= x;
		REG_BG0VOFS= y;
	}

    return 0;
}