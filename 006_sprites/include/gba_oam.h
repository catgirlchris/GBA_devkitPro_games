#ifndef __GBA_OAM__
#define __GBA_OAM__

#include "gba_types.h"

#define BFN_PREP(x, name)	( ((x)<<name##_SHIFT) & name##_MASK )
#define BFN_SET(y, x, name)	(y = ((y)&~name##_MASK) | BFN_PREP(x,name) )

INLINE void obj_set_pos(object_attributes_t *obj, int x, int y);



INLINE void obj_set_pos(object_attributes_t *obj, int x, int y)
{
	//BFN_SET(obj->attr0, y, ATTR0_Y);
	//BFN_SET(obj->attr1, x, ATTR1_X);
}

#endif