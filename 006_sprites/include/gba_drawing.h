#ifndef __GBA_DRAWING_H__
#define __GBA_DRAWING_H__

#include "gba_types.h"
#include "gba_reg.h"

#define SCREENBUFFER 		((v_u16*)(0x06000000))
#define SCREEN_W 			240
#define SCREEN_H 			160	

#define RGB(r,g,b)           (u16)(r + (g << 5) + (b << 10))

uint16_t setColor( unsigned char a_red, unsigned char a_green, unsigned char a_blue);

uint16_t MakeCol(uint8_t red, uint8_t green, uint8_t blue);

void draw_rectangle(int left, int top, int width, int height, uint16_t clr);

void drawLine(uint32_t a_x, uint32_t a_y, uint32_t a_x2, uint32_t a_y2, uint16_t a_colour);

void plotPixel(uint16_t x, uint16_t y, uint16_t colour);

#endif //__GBA_DRAWING_H__