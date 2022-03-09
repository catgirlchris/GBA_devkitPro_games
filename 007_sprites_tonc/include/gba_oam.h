#ifndef __GBA_OAM__
#define __GBA_OAM__

#include <tonc_types.h>

typedef struct object_attributes_t {
    u16 attr0;
    u16 attr1;
    u16 attr2;
    u16 pad;
} ALIGN4 object_attributes_t;

typedef u32 Tile[16];
typedef Tile TileBlock[256];

#define BFN_PREP(x, name)	( ((x)<<name##_SHIFT) & name##_MASK )
#define BFN_SET(y, x, name)	(y = ((y)&~name##_MASK) | BFN_PREP(x,name) )

INLINE void obj_set_pos(object_attributes_t *obj, int x, int y);



INLINE void obj_set_pos(object_attributes_t *obj, int x, int y)
{
	//BFN_SET(obj->attr0, y, ATTR0_Y);
	//BFN_SET(obj->attr1, x, ATTR1_X);
}

#endif