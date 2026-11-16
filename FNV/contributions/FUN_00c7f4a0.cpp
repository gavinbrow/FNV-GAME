static __declspec(noinline) unsigned char* FUN_00c7f4a0(unsigned char* out, const float* src, int count)
{
    int i = 0;
    if (count > 0)
    {
        do
        {
            float value = src[i];
            unsigned int bits = *(const unsigned int*)&value;
            if ((bits & 0x7f800000u) == 0x7f800000u)
            {
                *out = 0;
                return out;
            }
            ++i;
        } while (i < count);
    }
    *out = 1;
    return out;
}
unsigned char* S00c7f4a0_Call(unsigned char* out, const float* src, int count)
{
    return FUN_00c7f4a0(out, src, count);
}
