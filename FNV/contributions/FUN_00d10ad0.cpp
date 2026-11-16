void __fastcall FUN_00d10ad0(int a, void* b)
{
    int* p = (int*)b;
    int idx = a >> 5;
    int mask = 1 << (a & 0x1F);
    p[idx] ^= mask;
}
