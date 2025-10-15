#ifndef __GBA_MATHUTIL_H__
#define __GBA_MATHUTIL_H__

#include "gba_types.h"

extern s32 __gba_rand_seed;
extern s32 gba_seed_randomize(s32 a_val);
extern s32 gba_generate_random();
extern s32 gba_generate_random_range(s32 a_min, s32 a_max);
extern s32 sign(s32 a_val);
extern s32 abs(s32 a_val);
extern s32 min(s32 n1, s32 n2);
extern s32 max(s32 n1, s32 n2);

#endif //__GBA_MATHUTIL_H__