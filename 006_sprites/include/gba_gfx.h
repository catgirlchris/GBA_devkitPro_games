#ifndef __GBA_GFX_H__
#define __GBA_GFX_H__

#include "gba_macros.h"
#include "gba_reg.h"
#include "gba_types.h"

/* Base address pointer for base register */
#define REG_DISPCNT *((v_u32*)(REG_BASE))

//Defines for settng up different video modes
#define VIDEOMODE_0 0x0000  /* Sprite Mode 0 */
#define VIDEOMODE_1 0x0001  /* Sprite Mode 1 */
#define VIDEOMODE_2 0x0002  /* Sprite Mode 2 */
#define VIDEOMODE_3 0x0003	/* Sprite Mode 3 ; 240x160 @16bpp */
#define VIDEOMODE_4	0x0004	/* Sprite Mode 4 ; 240x160 @8 bpp */
#define VIDEOMODE_5 0x0005  /* Sprite Mode 5 */ 

//Defines for enabling different backgrounds
#define BGMODE_0	0x0100  /* Background Mode 0 */
#define BGMODE_1	0x0200  /* Background Mode 1 */
#define BGMODE_2	0x0400  /* Background Mode 2 */
#define BGMODE_3	0x0800  /* Background Mode 3 */

//Other fields
#define ENABLE_OBJECTS 0x1000
#define MAPPINGMODE_1D 0x0040

/* vcount is used for testing for vertical blank */
#define REG_VCOUNT (*(v_u16*)(REG_BASE + 0x06))

extern void vsync();

#endif //__GBA_GFX_H__