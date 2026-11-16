extern bool __cdecl SetSlotValueIfEmpty(int slot, int value);
extern "C" bool DAT_011dce50;
extern "C" void FUN_0082b8f0();

// @fnv 0x00f9d430
void __cdecl FUN_00f9d430()
{
    DAT_011dce50 = SetSlotValueIfEmpty(34, reinterpret_cast<int>(&FUN_0082b8f0));
}