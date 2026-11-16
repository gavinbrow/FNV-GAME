struct FUN_00d1edd0_stub
{
    void FUN_00d1edd0(const float* src);
};

void FUN_00d1edd0_stub::FUN_00d1edd0(const float* src)
{
    float a = src[0];
    float b = src[5];
    float c = a < b ? a : b;
    float d = src[10];
    float e = c < d ? c : d;
    *(float*)((char*)this + 0xc0) = e;
    *(float*)((char*)this + 0xc4) = e;
    *(float*)((char*)this + 0xc8) = e;
}