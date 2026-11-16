struct PixelChannels {
    unsigned int redMask;
    unsigned int greenMask;
    unsigned int blueMask;
    unsigned int alphaMask;
    unsigned char redRightShift;
    unsigned char greenRightShift;
    unsigned char blueRightShift;
    unsigned char alphaRightShift;
    unsigned char redLeftShift;
    unsigned char greenLeftShift;
    unsigned char blueLeftShift;
    unsigned char alphaLeftShift;
};

void __cdecl FUN_00a77630(
    unsigned int width,
    unsigned int height,
    unsigned int sourcePitch,
    char* output,
    unsigned int outputPitch,
    unsigned int unused,
    const unsigned int* source,
    const PixelChannels* channels)
{
    const unsigned int* pixel = source;
    if (height > 0) {
        unsigned int rowsRemaining = height;
        do {
            if (width > 0) {
                unsigned int pixelsRemaining = width;
                do {
                    *output++ = (char)((pixel[0] & channels->redMask)
                                      >> channels->redRightShift) << channels->redLeftShift;
                    *output++ = (char)((pixel[0] & channels->greenMask)
                                      >> channels->greenRightShift) << channels->greenLeftShift;
                    *output++ = (char)((pixel[0] & channels->blueMask)
                                      >> channels->blueRightShift) << channels->blueLeftShift;
                    *output++ = -1;
                    ++pixel;
                } while (--pixelsRemaining != 0);
            }
        } while (--rowsRemaining != 0);
    }
}