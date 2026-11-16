struct FUN_00d5f520_class {
    int unk00;
    int unk04;
    int unk08;
    int FUN_00d5f520(unsigned int a);
};

int FUN_00d5f520_class::FUN_00d5f520(unsigned int a)
{
    int v = unk08;
    if (v > 0)
    {
        unsigned int idx = ((a >> 4) * 0x9e3779b1) & (unsigned int)v;
        int val = *(int*)(*(int*)this + (idx << 4));
        while (val != -1)
        {
            if (val == (int)a)
                return (int)idx;
            idx = (idx + 1) & (unsigned int)v;
            val = *(int*)(*(int*)this + (idx << 4));
        }
    }
    return v + 1;
}
