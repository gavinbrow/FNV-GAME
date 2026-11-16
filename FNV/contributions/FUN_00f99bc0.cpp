// @fnv 0x00f99bc0
extern bool DAT_011dc3dd;
bool SetSlotValueIfEmpty(int slot, int value);
void FUN_0080f1a0();
void FUN_00f99bc0()
{
    DAT_011dc3dd = SetSlotValueIfEmpty(35, reinterpret_cast<int>(&FUN_0080f1a0));
}
