#include "ball.h"

void start_ball(struct ball* ball)
{
	ball->x_speed = ball->default_speed;
	ball->y_speed = ball->default_speed;;
	ball->n_bounces = 0;
	ball->bounce_speedup = 0;
	ball->x_collision_immunity_countdown = 0;
	ball->y_collision_immunity_countdown = 0;
	while ( ball->x_direction == 0)
		ball->x_direction = qran_range(-1, 2);
	while ( ball->y_direction == 0)
		ball->y_direction = qran_range(-1, 2);
}

void init_ball(struct ball* ball, s32 x, s32 y, s32 size, s32 speed, volatile struct object_attributes_t *obj_attributes)
{
	ball->x = x;
	ball->y = y;
	ball->size = size;
	ball->x_speed = speed;
	ball->y_speed = speed;
	ball->default_speed = speed;
	ball->x_direction = ball->y_direction = 0;
	ball->n_bounces = 0;
	ball->bounce_speedup = 0;
	ball->x_collision_immunity_countdown = 0;
	ball->y_collision_immunity_countdown = 0;

	ball->obj_attributes = obj_attributes;
	ball->obj_attributes->attr0 = 0x2000 | (0x1ff & y); // 8bpp tiles, SQUARE shape, at y coord 50
    ball->obj_attributes->attr1 = 0x4000 | (0x1ff & x); // 16x16 size when using the SQUARE shape
    ball->obj_attributes->attr2 = 2;      // Start at the first tile in tile

	start_ball(ball);
}

void move_ball(struct ball* ball)
{
	ball->y += ball->y_speed * ball->y_direction;
	if ( ball->y < 0)
	{
		ball->y = 0;
		bounce_ball_y(ball, 0);
	}
	if ( ball->y > SCREEN_HEIGHT - ball->size)
	{
		ball->y = SCREEN_HEIGHT - ball->size;
		bounce_ball_y(ball, 0);
	}

	ball->x += ball->x_speed*ball->x_direction;
	if ( ball->x < 0 || ball->x > SCREEN_WIDTH - ball->size)
	{
		ball->x = (SCREEN_WIDTH >> 1) - (ball->size >> 1);
		ball->y = (SCREEN_HEIGHT >> 1) - (ball->size >> 1);
		ball->x_direction = 0; ball->y_direction = 0;
		start_ball(ball);
	}

}

void bounce_ball(struct ball* ball)
{
	ball->n_bounces++;
	ball->x_direction *= -1;
}

void bounce_ball_test(struct ball* ball, bool flip_x_direction, bool flip_y_direction, s32 additional_x_speed, s32 additional_y_speed)
{
	ball->n_bounces++;
	if (ball->n_bounces == 6)
	{
		ball->x_speed += 1;
		ball->y_speed += 1;
	}

	ball->x_speed += additional_x_speed;
	ball->y_speed += additional_x_speed;

	if (flip_x_direction)
	{
		ball->x_direction *= -1;
	}
	if (flip_y_direction)
	{
		ball->y_direction *= -1;
	}
}

void bounce_ball_y(struct ball* ball, s32 y_additional_speed)
{
	ball->n_bounces++;
	ball->y_speed += ABS(y_additional_speed);
	ball->y_direction *= -1;
}

void draw_ball(struct ball* ball)
{
	ball->obj_attributes->attr0 = 0x2000 | (0x0FF & ball->y);
	ball->obj_attributes->attr1 = 0x4000 | (0x0FF & ball->x);
	//obj_set_pos(ball->obj_attributes, ball->x, ball->y);
}