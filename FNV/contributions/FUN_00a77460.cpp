extern "C" unsigned char DAT_00ff0000;
void __cdecl FUN_00a77460(unsigned int width, unsigned int height, int, unsigned char *dst, int, int, const unsigned char *src, const unsigned int *mask)
{
    if (mask[1] == 0xFF00) {
        if (mask[0] == (unsigned int)&DAT_00ff0000) {
            if (height > 0) {
                unsigned int rows = height;
                do {
                    if (width > 0) {
                        unsigned int cols = width;
                        do {
                            *dst++ = src[2];
                            *dst++ = src[1];
                            *dst++ = src[0];
                            *dst++ = 0xFF;
                            src += 3;
                        } while (--cols != 0);
                    }
                } while (--rows != 0);
            }
        } else {
            if (height > 0) {
                unsigned int rows = height;
                do {
                    if (width > 0) {
                        unsigned int cols = width;
                        do {
                            *dst++ = *src++;
                            *dst++ = *src++;
                            *dst++ = *src++;
                            *dst++ = 0xFF;
                        } while (--cols != 0);
                    }
                } while (--rows != 0);
            }
        }
    }
}