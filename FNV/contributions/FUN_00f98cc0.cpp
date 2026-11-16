// @fnv 0x00f98cc0
extern bool DAT_011dc108;
bool SetSlotValueIfEmpty(int slot, int value);
void FUN_0080d430();
void FUN_00f98cc0()
{
    DAT_011dc108 = SetSlotValueIfEmpty(22, reinterpret_cast<int>(&FUN_0080d430));
}
