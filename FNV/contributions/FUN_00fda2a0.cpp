namespace fnv_00a09330
{
    class FUN_00a09330_shell
    {
    public:
        void ClearActionsAndFreeBuffer();
    };
}

extern fnv_00a09330::FUN_00a09330_shell DAT_011f338c;

// @fnv 0x00fda2a0
extern "C" void __cdecl FUN_00fda2a0()
{
    DAT_011f338c.ClearActionsAndFreeBuffer();
}
