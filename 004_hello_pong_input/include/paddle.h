#ifndef __PONG_PADDLE_H__
#define __PONG_PADDLE_H__

#include "gba_types.h"
#include "ball.h"

struct paddle
{
	int32_t x, y, width, height;
	uint16_t colour;
};

void init_paddle(struct paddle* a_paddle, int32_t a_x, int32_t a_y, int32_t a_width, int32_t a_height, uint16_t a_colour);

void move_paddle(struct paddle* a_paddle, s32 a_val);

void draw_paddle(struct paddle* a_paddle);

void clear_paddle(struct paddle* a_paddle);

#endif //__PONG_PADDLE_H__