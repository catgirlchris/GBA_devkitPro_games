#include <stdint.h>
#include <stdbool.h>

#define REG_DISPLAYCONTROL 	*((volatile uint32_t*)(0x04000000))
#define VIDEOMODE_3 	   	0x0003
#define BGMODE_2    	   	0x0400

#define SCREENBUFFER 		((volatile uint16_t*)(0x06000000))
#define SCREEN_W 			240
#define SCREEN_H 			160
#define REG_VCOUNT      	(* (volatile uint16_t*) 0x04000006)

#define RGB(r,g,b) 			(uint16_t)(r + (g << 5) + (b << 10))

inline void vsync()
{
  while (REG_VCOUNT >= 160);
  while (REG_VCOUNT < 160);
}

int32_t abs(int32_t a_val)
{
	int32_t mask = a_val >> 31;
	return (a_val ^ mask) - mask;
}

uint16_t setColor( unsigned char a_red, unsigned char a_green, unsigned char a_blue)
{
	return (a_red & 0x1f) | (a_green & 0x1f) << 5 | (a_blue & 0x1f) << 10;
}

inline uint16_t MakeCol(uint8_t red, uint8_t green, uint8_t blue)
{
    return (red & 0x1F) | (green & 0x1F) << 5 | (blue & 0x1F) << 10;
}


void plotPixel(uint16_t x, uint16_t y, uint16_t colour)
{
	SCREENBUFFER[y * SCREEN_W + x] = colour;
}

void drawRect(int left, int top, int width, int height, uint16_t clr)
{
    for (int y = 0; y < height; ++y)
    {
        for (int x = 0; x < width; ++x)
        {
    	   SCREENBUFFER[(top + y) * SCREEN_W + left + x] = clr;
        }
    }
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

void fillScreen(uint16_t colour)
{
	drawRect(0, 0, SCREEN_W, SCREEN_H, colour);
}

int main()
{
	//set GBA rendering context to MODE 3 Bitmap Rendering
	REG_DISPLAYCONTROL = VIDEOMODE_3 | BGMODE_2;


	uint32_t i = 0;
	while(1){
		//wait until GBA stops drawing to the screen, nothing should be executing until it finishes.
		vsync();
		//fillScreen(RGB(0, 0, 0));

		drawLine(10, 4+i, 230, 4, setColor(31, 31, 31));
		drawLine(230, 156+i, 10, 156, setColor(31, 31, 31));

		drawLine(10, 4, 230, 156, setColor(2, 31, 15));
		drawLine(10, 156, 230, 4, setColor(2, 15, 31));

		i++;
		if (i>230)
			i = -i;
		
		//drawRect(15, 15, SCREEN_W-30, SCREEN_H-30, MakeCol(255, 70, 145));
	}

	return 0;
}