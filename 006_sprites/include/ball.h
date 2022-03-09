#ifndef __PONG_BALL_H__
#define __PONG_BALL_H__

#include "gba_types.h"
#include "paddle.h"


struct ball
{
	s32 x, y, x_direction, y_direction, size, x_speed, y_speed, default_speed, n_bounces, bounce_speedup, x_collision_immunity_countdown, y_collision_immunity_countdown;
	volatile object_attributes_t *obj_attributes;
};


void start_ball(struct ball* ball);
void init_ball(struct ball* ball, s32 x, s32 y, s32 size, s32 speed, volatile object_attributes_t *obj_attributes);

void move_ball(struct ball* ball);
void bounce_ball(struct ball* ball);
void bounce_ball_test(struct ball* ball, bool flip_x_direction, bool flip_y_direction, s32 additional_x_speed, s32 additional_y_speed);
void bounce_ball_y(struct ball* ball, s32 y_additional_speed);

void draw_ball(struct ball* ball);
void clear_ball(struct ball* ball);


#endif //__PONG_BALL_H__
