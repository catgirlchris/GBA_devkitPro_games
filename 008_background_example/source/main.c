#include <string.h>
#include <tonc_video.h>
#include <tonc_input.h>
#include <tonc_types.h>

#include "img/ball_sprite.h"
#include "img/ball_sprite.c"
#include "img/paddle_sprite.h"
#include "img/paddle_sprite.c"
#include "img/pong_paddle.h"
#include "img/pong_paddle.c"



int main()
{
    memcpy(pal_obj_mem, pong_paddlePal,  pong_paddlePalLen );
    memcpy(&tile8_mem[4][1], ball_spriteTiles, ball_spriteTilesLen);

    //memcpy(pal_obj_mem, paddle_spritePal,  paddle_spritePalLen );
    memcpy(&tile8_mem[4][5], pong_paddleTiles, pong_paddleTilesLen);


    REG_DISPCNT =  DCNT_MODE0 | DCNT_OBJ | DCNT_OBJ_1D;

    

    while(1)
    {
        // wait vblank
        vid_vsync();

        key_poll();

        // update
    }

    return 0;
}