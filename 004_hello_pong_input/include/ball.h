#ifndef __PONG_BALL_H__
#define __PONG_BALL_H__

#include "gba_types.h"

#include "paddle.h"

struct ball
{
	int32_t x, y, xDir, yDir, size;
	uint16_t colour;
};


void start_ball(struct ball* a_ball);
void init_ball(struct ball* a_ball, int32_t a_x, int32_t a_y, int32_t a_size, int16_t a_colour);

void move_ball(struct ball* a_ball);
void bounce_ball(struct ball* a_ball);

void draw_ball(struct ball* a_ball);
void clear_ball(struct ball* a_ball);


#endif //__PONG_BALL_H__
