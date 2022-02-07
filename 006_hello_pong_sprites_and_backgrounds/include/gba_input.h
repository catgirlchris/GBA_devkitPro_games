#include "gba_types.h"
#include "gba_reg.h"
#include "gba_macros.h"

#ifndef __GBA_INPUT__
#define __GBA_INPUT__

#define REG_KEYINPUT	*(v_u16*)(REG_BASE + 0x130)
#define REG_KEYCNT		*(v_u16*)(REG_BASE + 0x132)

#define KEY_MASK        0x03FF

enum KEYS
{
    A       = (1 << 0),
    B       = (1 << 1),
    SELECT  = (1 << 2),
    START   = (1 << 3),
    RIGHT   = (1 << 4),
    LEFT    = (1 << 5),
    UP      = (1 << 6),
    DOWN    = (1 << 7),
    R       = (1 << 8),
    L       = (1 << 9),

    KEYIRQ_ENABLE   = (1 << 14),
    KEYIRQ_OR       = (0 << 15),
    KEYIRQ_AND      = (1 << 15),
};

extern u16 __current_keys, __previous_keys;

inline void poll_keys()
{
    __previous_keys = __current_keys;
    __current_keys = ~REG_KEYINPUT & KEY_MASK;
}

inline u16 current_key_state()      {return __current_keys;  }
inline u16 previous_key_state()     {return __previous_keys; }

/*
If we want to ask if two keys are down at the same time we can use:

+--------------------------------+
| if( keyDown(A) && keyDown(B) ) |
| {                              |
|    //do something...           |
| }                              |
+--------------------------------+

    Although this is a bit wastefull calling the function twice, 
 fortunately the way that this code is written we can do a little better
 by making use of a *bitwise OR (	)*


+---------------------------------+
| if( keyDown( A | B ) == (A|B) ) |
| {                               |
|    //do something...            |
| }                               |
+---------------------------------+ */


inline u16 key_down(u16 a_key)      {return __current_keys  & a_key; }
inline u16 key_up(u16 a_key)        {return ~__current_keys & a_key; }

inline u16 key_held(u16 a_key)      {return (__current_keys  & __previous_keys  & a_key); }
inline u16 key_released(u16 a_key)  {return (~__current_keys & __previous_keys  & a_key); }
inline u16 key_hit(u16 a_key)       {return (__current_keys  & ~__previous_keys & a_key); }

inline u16 key_state_change(u16 a_key) { return (__current_keys ^ __previous_keys) & a_key; }


enum AXIS
{
	HORIZONTAL = 0,
	VERTICAL,

};

inline s16 get_axis(enum AXIS a_val)
{
	switch (a_val)
	{
	case HORIZONTAL:
		//shift __currKeys down 4 to move the value for RIGHT to the lowest bit & with 1 do the same for LEFT and subtract
		//if right is pressed the equation becomes 1 - 0 = 1, if Left is pressed then 0 - 1 = -1.
		return ((__current_keys >> 4) & 1) - ((__current_keys >> 5) & 1);
	case VERTICAL:
		//This is the same logic as above however uses UP and DOWN.
		return ((__current_keys >> 6) & 1) - ((__current_keys >> 7) & 1);
	default:
		return 0;
	}
}

#endif