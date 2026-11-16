extern unsigned char DAT_0080ef50;
extern bool DAT_011dc33c;
bool __cdecl SetSlotValueIfEmpty(int first, int second);

// @fnv 0x00f99940
extern "C" void __cdecl FUN_00f99940()
{
    DAT_011dc33c = SetSlotValueIfEmpty(13, reinterpret_cast<int>(&DAT_0080ef50));
}