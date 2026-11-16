extern unsigned char DAT_0080e4c0;
extern bool DAT_011dc2e8;
bool __cdecl SetSlotValueIfEmpty(int first, int second);

// @fnv 0x00f996c0
extern "C" void __cdecl FUN_00f996c0()
{
    DAT_011dc2e8 = SetSlotValueIfEmpty(11, reinterpret_cast<int>(&DAT_0080e4c0));
}