#include "gba_gfx.h"

/**
 * @brief Waits until the GBA system stops drawing to the screen.
 * For now the performance is not good as it isnt using interrupts.
 */
void vsync()
{
	while (_REG_VCOUNT >= 160);
	while (_REG_VCOUNT < 160);
}