#include "gba_types.h"
#include "gba_gfx.h"
#include "gba_mathUtil.h"
#include "gba_drawing.h"
#include "gba_input.h"
#include "gba_bios.h"

#include "ball.h"
#include "paddle.h"

#include "img_gba_pong_menu.h"

#include <string.h>

/**
 * @brief Comprueba la colision entre a_paddle y a_ball.
 * 
 * @param a_paddle La pala.
 * @param a_ball La bola.
 * @return true si están colisionando y false si no.
 */
bool check_collisions(struct paddle* a_paddle, struct ball* a_ball)
{
	if (a_paddle->x < a_ball->x+a_ball->size && a_paddle->x+a_paddle->width > a_ball->x)
	{
		if (a_paddle->y < a_ball->y+a_ball->size && a_paddle->y+a_paddle->height > a_ball->y)
			return true;
	}
	return false;
}


int main()
{
	//set GBA rendering context to MODE 3 Bitmap Rendering
	REG_DISPCNT = VIDEOMODE_3 | BGMODE_2;
	

	//set up GBA registers so VBLANK interrupts are sent
	register_vblank_isr(); 

	//test ball
	gba_seed_randomize(23343);
	struct ball ball;
	init_ball( &ball, SCREEN_W >> 1, SCREEN_H >> 1, 10, RGB(31, 31, 31));

	struct paddle paddle1;
	init_paddle( &paddle1, 10, 60, 16, 16, RGB(0, 0, 31));

	struct paddle paddle2;
	init_paddle( &paddle2, SCREEN_W - 18, 60, 16, 16, RGB(31, 0, 0));
	//init_paddle( &paddle2, SCREEN_W - 18, 0, 16, SCREEN_H, RGB(31, 0, 0));

	s32 paddle1_dir = 0;

	while(1)
	{
		//wait until GBA stops drawing to the screen, nothing should be executing until it finishes.
		vblank_interrupt_wait();
		poll_keys();

		// remove draw from last frame
		clear_ball(&ball);
		clear_paddle(&paddle1);
		clear_paddle(&paddle2);

		//update data
		move_ball(&ball);
		
		
		// check collisions on both paddles
		if (check_collisions(&paddle1, &ball))
			bounce_ball(&ball);
		if (check_collisions(&paddle2, &ball))
			bounce_ball(&ball);
		
		move_paddle(&paddle2, (abs(ball.yDir)/ball.yDir)*1);

		paddle1_dir = 0;
		if (key_down(DOWN))
		{
			move_paddle(&paddle1, 2);
			paddle1_dir = 1;
		}
		else if (key_down(UP))
		{
			move_paddle(&paddle1, -2);
			paddle1_dir = -1;
		}
		if (key_down(A))
		{
			move_paddle(&paddle1, paddle1_dir*70);
		}

		//draw
		draw_ball(&ball);
		draw_paddle(&paddle1);
		draw_paddle(&paddle2);
	}

	return 0;
}