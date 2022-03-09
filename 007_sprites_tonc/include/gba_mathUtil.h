#ifndef __GBA_MATHUTIL_H__
#define __GBA_MATHUTIL_H__


#include <tonc_types.h>

extern s32 __gba_rand_seed;
extern s32 gba_seed_randomize(s32 a_val);
extern s32 gba_generate_random();
extern s32 gba_generate_random_range(s32 a_min, s32 a_max);
extern s32 gba_sign(s32 a_val);
extern s32 gba_abs(s32 a_val);
extern s32 gba_min(s32 n1, s32 n2);
extern s32 gba_max(s32 n1, s32 n2);

#endif //__GBA_MATHUTIL_H__