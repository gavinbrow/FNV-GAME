namespace fnv_00526100
{
    class GlobalObject2_0040c150
    {
    public:
        int* Int();
    };
}

extern fnv_00526100::GlobalObject2_0040c150 DAT_011c9fb8;
extern int DAT_011c9f6c;

// @fnv 0x00f4b250
void FUN_00f4b250()
{
    DAT_011c9f6c = *DAT_011c9fb8.Int();
}
