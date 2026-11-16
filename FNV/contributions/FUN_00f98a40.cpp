// @fnv 0x00f98a40
extern bool DAT_011dc035;
bool SetSlotValueIfEmpty(int slot, int value);
void FUN_0080d120();
void FUN_00f98a40()
{
    DAT_011dc035 = SetSlotValueIfEmpty(20, reinterpret_cast<int>(&FUN_0080d120));
}
