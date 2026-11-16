// @fnv 0x00f987c0
extern bool DAT_011dc004;
bool SetSlotValueIfEmpty(int slot, int value);
void FUN_0080cc70();
void FUN_00f987c0()
{
    DAT_011dc004 = SetSlotValueIfEmpty(7, reinterpret_cast<int>(&FUN_0080cc70));
}
