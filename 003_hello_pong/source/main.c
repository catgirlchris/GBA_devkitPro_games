#include "gba_types.h"
#include "gba_gfx.h"
#include "gba_mathUtil.h"
#include "gba_drawing.h"

#include "ball.h"
#include "paddle.h"


int main()
{
	//set GBA rendering context to MODE 3 Bitmap Rendering
	REG_DISPCNT = VIDEOMODE_3 | BGMODE_2;

	//test ball
	gba_seed_randomize(23343);
	struct ball ball;
	init_ball( &ball, SCREEN_W >> 1, SCREEN_H >> 1, 10, RGB(31, 31, 31));

	struct paddle paddle1;
	init_paddle( &paddle1, 10, 60, 8, 40, RGB(0, 0, 31));

	struct paddle paddle2;
	init_paddle( &paddle2, SCREEN_W - 18, 60, 8, 40, RGB(31, 0, 0));

	while(1)
	{
		//wait until GBA stops drawing to the screen, nothing should be executing until it finishes.
		vsync();
		// remove draw from last frame
		clear_ball(&ball);
		clear_paddle(&paddle1);
		clear_paddle(&paddle2);

		//update data
		move_ball(&ball);

		//draw
		draw_ball(&ball);
		draw_paddle(&paddle1);
		draw_paddle(&paddle2);
	}

	return 0;
}