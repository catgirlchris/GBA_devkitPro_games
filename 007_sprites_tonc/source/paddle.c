#include "paddle.h"

void init_paddle(struct paddle* paddle, s32 x, s32 y, s32 width, s32 height, s32 speed, volatile object_attributes_t *obj_attributes)
{
	paddle->x = x;
	paddle->y = y;
	paddle->width = width;
	paddle->height = height;
	paddle->speed = speed;
	paddle->y_direction = 0;

	paddle->obj_attributes = obj_attributes;
	paddle->obj_attributes->attr0 = 0xA000 | (0x1FF & y); // 8bpp tiles, WIDE shape, at y coord 50
    paddle->obj_attributes->attr1 = 0x4000 | (0x1FF & x); // 8x32 size when using the WIDE shape
    paddle->obj_attributes->attr2 = 10;      			 // Start at the first tile in tile
}

void move_paddle_by_value(struct paddle* paddle, s32 val)
{
	paddle->y += val;
	if (paddle->y < 0)
	{
		paddle->y = 0;
	}
	if (paddle->y > SCREEN_HEIGHT - paddle->height)
	{
		paddle->y = SCREEN_HEIGHT - paddle->height;
	}
}

void move_paddle(struct paddle* paddle)
{
	move_paddle_by_value(paddle, paddle->y_direction*paddle->speed);
}

void draw_paddle(struct paddle* paddle)
{
	paddle->obj_attributes->attr0 = 0xA000 | (0x1FF & paddle->y);
	paddle->obj_attributes->attr1 = (paddle->obj_attributes->attr1 & 0xFF00) | (0x00FF & paddle->x);
}