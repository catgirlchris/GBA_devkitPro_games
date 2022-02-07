#include "ball.h"
#include "gba_mathUtil.h"
#include "gba_drawing.h"



void start_ball(struct ball* a_ball)
{
	while ( a_ball->xDir == 0)
	{
		a_ball->xDir = gba_generate_random_range(-1, 2);
	}
	a_ball->yDir = gba_generate_random_range(-1, 2);
}

void init_ball(struct ball* a_ball, int32_t a_x, int32_t a_y, int32_t a_size, int16_t a_colour)
{
	a_ball->x = a_x;
	a_ball->y = a_y;
	a_ball->size = a_size;
	a_ball->colour = a_colour;
	a_ball->xDir = a_ball->yDir = 0;
	start_ball(a_ball);
}

void move_ball(struct ball* a_ball)
{
	a_ball->y += a_ball->yDir;
	if ( a_ball->y < 0)
	{
		a_ball->y = 0;
		a_ball->yDir *= -1;
	}
	if ( a_ball->y > SCREEN_H - a_ball->size)
	{
		a_ball->y = SCREEN_H - a_ball->size;
		a_ball->yDir *= -1;
	}

	a_ball->x += a_ball->xDir;
	if ( a_ball->x < 0 || a_ball->x > SCREEN_W - a_ball->size)
	{
		a_ball->x = (SCREEN_W >> 1) - (a_ball->size >> 1);
		a_ball->y = (SCREEN_H >> 1) - (a_ball->size >> 1);
		a_ball->xDir = 0; a_ball->yDir = 0;
		start_ball(a_ball);
	}

}

void draw_ball(struct ball* a_ball)
{
	draw_rectangle(a_ball->x, a_ball->y, a_ball->size, a_ball->size, a_ball->colour);
}

void clear_ball(struct ball* a_ball)
{
	draw_rectangle(a_ball->x, a_ball->y, a_ball->size, a_ball->size, RGB(0, 0, 0));
}