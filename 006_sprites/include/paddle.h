#ifndef __PONG_PADDLE_H__
#define __PONG_PADDLE_H__

#include "gba_types.h"
#include "ball.h"

struct paddle
{
	s32 x, y, width, height, y_direction, speed;

	volatile object_attributes_t *obj_attributes;
};

void init_paddle(struct paddle* paddle, s32 x, s32 y, s32 width, s32 height, s32 speed, volatile object_attributes_t *obj_attributes);

void move_paddle_by_value(struct paddle* paddle, s32 val);

void move_paddle(struct paddle* paddle);

void draw_paddle(struct paddle* paddle);

void clear_paddle(struct paddle* paddle);

#endif //__PONG_PADDLE_H__