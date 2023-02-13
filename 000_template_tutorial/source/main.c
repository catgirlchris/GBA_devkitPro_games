//#include "Intellisense.h"

#define REG_DISPCNT *((unsigned int*)(0x04000000))
#define VIDEOMODE_3 0x0003
#define BG_ENABLE2  0x0400

int main()
{
	//set GBA rendering context to MODE 3 Bitmap Rendering
	REG_DISPCNT = VIDEOMODE_3 | BG_ENABLE2;

	int t = 0;
	while(1){
		int x,y;
		for(x = 0; x < 240; ++x){
			for( y = 0; y < 160; ++y){
				((unsigned short*)0x06000000)[x+y*240] = ((((x&y)+t) & 0x1F) << 10)|
				((((x&y)+t*3)&0x1F)<<5) | ((((x&y)+t * 5)&0x1F)<<0);
			}
		}
		++t;
	}
	return 0;
}