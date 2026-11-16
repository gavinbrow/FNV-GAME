void __cdecl FUN_00e520b0(const float* src, unsigned char* dst)
{
    unsigned char channel[4];
    unsigned int i = 0;
    channel[0] = (unsigned char)(7 - (unsigned char)(int)(src[i++] * -7.0));
    channel[1] = (unsigned char)(7 - (unsigned char)(int)(src[i++] * -7.0));
    channel[2] = (unsigned char)(7 - (unsigned char)(int)(src[i++] * -7.0));
    channel[3] = (unsigned char)(7 - (unsigned char)(int)(src[i] * -7.0));
    dst[0] = (unsigned char)(channel[0] | (channel[1] << 4));
    dst[1] = (unsigned char)(channel[2] | (channel[3] << 4));
}