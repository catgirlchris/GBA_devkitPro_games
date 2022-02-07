#include "gba_drawing.h"

#include "paddle.h"


void init_paddle(struct paddle* a_paddle, int32_t a_x, int32_t a_y, int32_t a_width, int32_t a_height, uint16_t a_colour)
{
	a_paddle->x = a_x;
	a_paddle->y = a_y;
	a_paddle->width = a_width;
	a_paddle->height = a_height;
	a_paddle->colour = a_colour;
}

void draw_paddle(struct paddle* a_paddle)
{
	draw_rectangle(a_paddle->x, a_paddle->y, a_paddle->width, a_paddle->height, a_paddle->colour);
}

void clear_paddle(struct paddle* a_paddle)
{
	draw_rectangle(a_paddle->x, a_paddle->y, a_paddle->width, a_paddle->height, RGB(0,0,0));
}