#include "gba_gfx.h"
#include "gba_input.h"
#include "gba_mathUtil.h"
#include "gba_reg.h"
#include "ball.h"
#include "paddle.h"

#include <string.h>
//#include <tonc_input.h>
#include <tonc_types.h>

#include "img/ball_sprite.h"
#include "img/ball_sprite.c"
#include "img/paddle_sprite.h"
#include "img/paddle_sprite.c"
#include "img/pong_paddle.h"
#include "img/pong_paddle.c"

#define _MEM_VRAM      ((v_u16*)0x6000000)
#define MEM_TILE      ((TileBlock*)0x6000000 )
#define MEM_PALETTE   ((u16*)(0x05000200))


bool check_collisions(struct paddle* paddle, struct ball* ball)
{
	if (paddle->x < ball->x+ball->size && paddle->x+paddle->width > ball->x)
	{
		if (paddle->y < ball->y+ball->size && paddle->y+paddle->height > ball->y)
        {
			return true;
        }
	}
	return false;
}

bool check_collisions_next_frame(struct paddle* paddle, struct ball* ball)
{
	if ((paddle->x  <  ball->x + ball->x_direction*ball->x_speed + ball->size)   
        &&  (paddle->x + paddle->width  >  ball->x + ball->x_direction*ball->x_speed))
	{
        /* TODO Para tratar que la pala puede no estar moviendose, puedo usas min() y max() */
		if ((paddle->y - paddle->speed /*- 8*/  <  ball->y + ball->size + ball->y_speed /*+ 8*/)  
            &&  (paddle->y+paddle->height+paddle->speed /*+ 8*/ >  ball->y - ball->y_speed /*- 8*/))
        {
			return true;
        }
	}
	return false;
}

void clamp_right(struct paddle* paddle, struct ball* ball)
{
    if ((ball->x >= paddle->x+paddle->width) || (ball->x+ball->size <= paddle->x))
        ball->x = paddle->x+paddle->width+ball->size;
}
void clamp_left(struct paddle* paddle, struct ball* ball)
{
    if ((ball->x >= paddle->x+paddle->width) || (ball->x+ball->size <= paddle->x))
        ball->x = paddle->x-ball->size;
}

int main()
{
    memcpy(MEM_PALETTE, pong_paddlePal,  pong_paddlePalLen );
    memcpy(&MEM_TILE[4][1], ball_spriteTiles, ball_spriteTilesLen);

    //memcpy(MEM_PALETTE, paddle_spritePal,  paddle_spritePalLen );
    memcpy(&MEM_TILE[4][5], pong_paddleTiles, pong_paddleTilesLen);

    gba_seed_randomize(23343);

    struct ball ball;
    init_ball(&ball, SCREEN_W >> 1, SCREEN_H >> 1, 8, 1, &OAM[0]);

    struct paddle paddle;
    init_paddle(&paddle, 16, SCREEN_H >> 1, 8, 32, 3, &OAM[1]);

    struct paddle paddle_enemy;
    init_paddle(&paddle_enemy, SCREEN_W - 16 - 8, ball.y, 8, 32, 3, &OAM[2]);
    paddle_enemy.obj_attributes->attr1 |= 0x3000;



    _REG_DISPCNT =  VIDEOMODE_0 | ENABLE_OBJECTS | MAPPINGMODE_1D;

    

    while(1)
    {
        // wait vblank
        vsync();

        poll_keys();

        // update
        move_ball(&ball);

        paddle.y_direction = 0;
        paddle.speed = 0;
        if (key_down(DOWN))
        {
            paddle.y_direction = 1;
            paddle.speed = 3;
        }
        else if (key_down(UP))
        {
            paddle.y_direction = -1;
            paddle.speed = 3;
        }

        if (ball.x_collision_immunity_countdown > 0 || ball.y_collision_immunity_countdown > 0)
            paddle.speed = 0;
        
        move_paddle(&paddle);

        move_paddle_by_value(&paddle_enemy, ball.y_direction);

        /* If ball collisioned with paddle recently, decrease countdown. */
        if (ball.x_collision_immunity_countdown > 0)
		    ball.x_collision_immunity_countdown--;
        if (ball.y_collision_immunity_countdown > 0)
		    ball.y_collision_immunity_countdown--;

        /* Process paddle <-> ball collision */
        if (ball.x_collision_immunity_countdown > 0 && ball.y_collision_immunity_countdown > 0)
            ;
        else if (check_collisions_next_frame(&paddle, &ball))
        {
            /* if paddle-top is below ball_bot  */
            if ((paddle.y >= ball.y+ball.size) /*&& (ball.y+ball.size+ball.y_direction > paddle.y)*/)
            {
                if (ball.y_collision_immunity_countdown == 0)
                    bounce_ball_y(&ball, 1+gba_abs(paddle.y_direction)*1);
                ball.y = gba_min(ball.y, paddle.y-ball.size - paddle.speed -ball.y_speed /*- 4*/);
                ball.y_collision_immunity_countdown = 10;
            } /* if paddle_bot is above */
            else if (paddle.y+paddle.height <= ball.y)
            {
                if (ball.y_collision_immunity_countdown == 0)
                    bounce_ball_y(&ball, 1+gba_abs(paddle.y_direction)*1);
                ball.y = gba_max(ball.y, paddle.y + paddle.height + paddle.speed + ball.y_speed /*+ 4*/);
                ball.y_collision_immunity_countdown = 10;
            }
            else
            {
                if (ball.x_collision_immunity_countdown == 0)
                    bounce_ball_test(&ball, true, false, 0, 0);
                if (paddle.y_direction)
                    ball.y_direction = paddle.y_direction;
                //ball.x_collision_immunity_countdown = 60;
            }
        }

        /* Process paddle_enemy <-> ball collision */
        if (check_collisions_next_frame(&paddle_enemy, &ball))
        {
            bounce_ball(&ball);
        }

        // draw
        draw_ball(&ball);
        draw_paddle(&paddle);
        draw_paddle(&paddle_enemy);
    }

    return 0;
}