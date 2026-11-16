void* CreateFUN0082cf80(int a, int b, int c);
bool SetSlotValueIfEmpty(int slot, int value);
extern "C" bool DAT_011dcf74;

// @fnv 0x00f9d930
void FUN_00f9d930()
{
    DAT_011dcf74 = SetSlotValueIfEmpty(29, reinterpret_cast<int>(&CreateFUN0082cf80));
}
