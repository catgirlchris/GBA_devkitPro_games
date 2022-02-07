#include "gba_drawing.h"
#include "gba_mathUtil.h"

uint16_t setColor( unsigned char a_red, unsigned char a_green, unsigned char a_blue)
{
	return (a_red & 0x1f) | (a_green & 0x1f) << 5 | (a_blue & 0x1f) << 10;
}

uint16_t MakeCol(uint8_t red, uint8_t green, uint8_t blue)
{
    return (red & 0x1F) | (green & 0x1F) << 5 | (blue & 0x1F) << 10;
}

void draw_rectangle(int left, int top, int width, int height, uint16_t clr)
{
    for (int y = 0; y < height; ++y)
    {
        for (int x = 0; x < width; ++x)
        {
    	   SCREENBUFFER[(top + y) * SCREEN_W + left + x] = clr;
        }
    }
}

void plotPixel(uint16_t x, uint16_t y, uint16_t colour)
{
	SCREENBUFFER[y * SCREEN_W + x] = colour;
}

void drawLine(uint32_t a_x, uint32_t a_y, uint32_t a_x2, uint32_t a_y2, uint16_t a_colour)
{
	//Get the horizontal and vertical displacement of the line
	int32_t w = a_x2 - a_x; //w is width or horizontal distance
	int32_t h = a_y2 - a_y; //h is the height or vertical displacement
	//work out what the change in x and y is with the d in these variables stands for delta
	int32_t dx1 = 0, dy1 = 0, dx2 = 0, dy2 = 0;

	if (w<0) dx1 = dx2 = -1; else if (w>0) dx1 = dx2 = 1;
	if (h<0) dy1 = -1; else if (h>0) dy1 = 1;
	//which is the longest the horizontal or vertical step
	int32_t longest = abs(w); //assume that width is the longest displacement
	int32_t shortest = abs(h);
	if ( shortest > longest )	//oops it's the other way around reverse it
	{
		//use xor to swap longest and shortest around
		longest ^= shortest; shortest ^= longest; longest ^= shortest;
		if (h<0) dy2 = -1; else if (h>0) dy2 = 1;
		dx2 = 0;
	}
	//geta  value that is half the longest displacement
	int32_t numerator = longest >> 1;
	//for each pixel across the longest span
	for (int32_t i = 0; i <= longest; ++i)
	{
		//fill the pixel we're currently at
		plotPixel( a_x, a_y, a_colour);
		//increase the numerator by the shortest span
		numerator += shortest;
		if (numerator>longest)  
		{
			//if the numerator is now larger than the longest span
			//subtract the longest value from the numerator
			numerator -= longest;
			//increment x & y by their delta1 values
			a_x += dx1;
			a_y += dy1;
		}
		else 
		{
			//numerator is smaller than the longst side
			//increment x & y by their delta 2 values
			a_x += dx2;
			a_y += dy2;
		}
	}
}