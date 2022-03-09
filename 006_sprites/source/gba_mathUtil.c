#include "gba_mathUtil.h"

s32 __gba_random_seed = 42;

//Receives a seed so it can be used to generate new random values.
s32 gba_seed_randomize(s32 a_val)
{
	s32 old_seed = __gba_random_seed;
	__gba_random_seed = a_val;
	return old_seed;
}

//Generate a random value using LCG values taken from the Numerical Recipes Book
s32 gba_generate_random()
{
	__gba_random_seed = 1664525 * __gba_random_seed + 1013904223;
	return (__gba_random_seed >> 16) & 0x7fff;
}

//Random value within a range
s32 gba_generate_random_range(s32 a_min, s32 a_max)
{
	return (gba_generate_random() * (a_max - a_min) >> 15) + a_min;
}

s32 sign(s32 a_val)
{
	return (!(a_val & 0x80000000) && !a_val) ? 1 : -1;
}

s32 abs(s32 a_val)
{
	s32 mask = a_val >> 31;
	return (a_val ^ mask) - mask;
}

s32 min(s32 n1, s32 n2)
{
	if (n1 <= n2)
		return n1;
	else
		return n2;
}

s32 max(s32 n1, s32 n2)
{
	if (n1 >= n2)
		return n1;
	else
		return n2;
}