#ifndef __GBA_BIOS_H__
#define __GBA_BIOS_H__

#include "gba_reg.h"
#include "gba_macros.h"
#include <tonc_types.h>

/* +------------------------------------------------+
 * | 0 LCD V-Blank                      (0=Disable) |
 * | 1 LCD H-Blank                      (etc.)      |
 * | 2 LCD V-Counter Match              (etc.)      |
 * | 3 Timer 0 Overflow                 (etc.)      |
 * | 4 Timer 1 Overflow                 (etc.)      |
 * | 5 Timer 2 Overflow                 (etc.)      |
 * | 6 Timer 3 Overflow                 (etc.)      |
 * | 7 Serial Communication             (etc.)      |
 * | 8 DMA 0                            (etc.)      |
 * | 9 DMA 1                            (etc.)      |
 * | 10 DMA 2                           (etc.)      |
 * | 11 DMA 3                           (etc.)      |
 * | 12 Keypad                          (etc.)      |
 * | 13 Game Pak (external IRQ source)  (etc.)      |
 * | 14-15 Not used                                 |
 * +------------------------------------------------+ */
//Defines for Interrupts
//There are 14 Interrupts that we can register with REG_IE
#define INT_VBLANK 	0x0001
#define INT_HBLANK 	0x0002
#define INT_VCOUNT 	0x0004
#define INT_TIMER0 	0x0008
#define INT_TIMER1 	0x0010
#define INT_TIMER2 	0x0020
#define INT_TIMER3 	0x0040
#define INT_COM 	0x0080
#define INT_DMA0 	0x0100
#define INT_DMA1	0x0200
#define INT_DMA2 	0x0400
#define INT_DMA3 	0x0800
#define INT_BUTTON 	0x1000
#define INT_CART 	0x2000
//create pointer to video memory
#define DSTAT_VBL_IRQ 0x0008
#define DSTAT_VHB_IRQ 0x0010
#define DSTAT_VCT_IRQ 0x0020

/* Registro IME: Interrupt Master Enable.
 * Con 0 desactiva todos los interrupts, con valor 1 permite que se puedan activar.
 * 
 * #Nota: ponerlo a 1 no significa que los interrupts se vayan a activar. */
#define REG_IME         (*(vu32*)0x4000208)

/* Registro IE: Interrupt Enable Register */
#define REG_IE          (*(vu16*)0x4000200)
/* Registro IF: Interrupt Request Flag Register */
#define REG_IF          (*(vu16*)0x4000202)

/* Registro DIPSTAT: Display Status and Interrupt Control. 
 * Si queremos usar los interrupts de la pantalla necesitamos registrarlos aquí también.
 * Si no, no se lanzan.  */
#define REG_DISPSTAT    (*(vu16*)0x4000004)

/* REG_INTERRUPT this memory address is where the interrupt funciton pointer will be stored 
 *
 * */
#define REG_INTERRUPT *(fnptr*)(0x03007FFC)

/* REG_IFBIOS this is the BIOS register address that needs to be set to inform the bios 
 * that any interrupts it was expecting have been dealt with.
 *   */
#define REG_IFBIOS (*(vu16*)(0x3007FF8))





typedef void (*fnptr)(void);

//This is the declaration for the function we will call to trigger the VBLANK interrupt wait
void vblank_interrupt_wait();

//This is the function that will be called by the CPU when an interrupt is triggered
ARM void interrupt_handler();


/**
 * @brief This is the function that we wil call to register that we want to register a VBLANK Interrupt
 * ISR significa Interrupt Service Routine.
 */
void register_vblank_isr();


#endif