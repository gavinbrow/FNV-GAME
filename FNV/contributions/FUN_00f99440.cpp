extern unsigned char DAT_0080df10;
extern bool DAT_011dc21c;
bool __cdecl SetSlotValueIfEmpty(int first, int second);

// @fnv 0x00f99440
extern "C" void __cdecl FUN_00f99440()
{
    DAT_011dc21c = SetSlotValueIfEmpty(8, reinterpret_cast<int>(&DAT_0080df10));
}