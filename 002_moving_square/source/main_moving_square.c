typedef unsigned char      uint8;
typedef unsigned short     uint16;
typedef unsigned int       uint32;

#define REG_DISPLAYCONTROL *((volatile uint32*)(0x04000000))
#define VIDEOMODE_3         0x0003
#define BGMODE_2            0x0400

#define SCREENBUFFER        ((volatile uint16*)0x06000000)
#define SCREEN_W            240
#define SCREEN_H            160
#define REG_VCOUNT      (* (volatile uint16*) 0x04000006)


inline void vsync()
{
  while (REG_VCOUNT >= 160);
  while (REG_VCOUNT < 160);
}


inline uint16 MakeCol(uint8 red, uint8 green, uint8 blue)
{
    return (red & 0x1F) | (green & 0x1F) << 5 | (blue & 0x1F) << 10;
}

void drawRect(int left, int top, int width, int height, uint16 clr)
{
    for (int y = 0; y < height; ++y)
    {
        for (int x = 0; x < width; ++x)
        {
    	   SCREENBUFFER[(top + y) * SCREEN_W + left + x] = clr;
        }
    }
}

int main()
{
    REG_DISPLAYCONTROL = VIDEOMODE_3 | BGMODE_2;

    for (int i = 0; i < SCREEN_W * SCREEN_H; ++i)
    {
    	SCREENBUFFER[i] = MakeCol(0,0,0);
    }

    int x = 0;
	while (1)
	{
		vsync();

		if (x > SCREEN_W * (SCREEN_H / 10))
			x = 0;
		if (x)
		{
			int last = x - 10;
			drawRect(last % SCREEN_W, (last / SCREEN_W) * 10, 10, 10, MakeCol(0, 0, 0));
		}

		drawRect(x % SCREEN_W, (x / SCREEN_W) * 10, 10, 10, MakeCol(31, 31, 31));
		x += 10;
	}

	return 0;
}