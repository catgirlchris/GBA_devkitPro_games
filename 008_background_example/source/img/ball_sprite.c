#include "img/ball_sprite.h"

const unsigned int ball_spriteTiles[16] __attribute__((aligned(4)))=
{
    0x01010101,0x01010101,0x01010101,0x01010101,0x01010101,0x01010101,0x01010101,0x01010101,
    0x01010101,0x01010101,0x01010101,0x01010101,0x01010101,0x01010101,0x01010101,0x01010101,
    /*0x000000001,0x00000000,0x0000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,
    0x000000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,*/
};

const unsigned int ball_spritePal[3] __attribute__((aligned(4)))=
{
    0x001E0000,0x03E07FFF,0x00007C1F,
};