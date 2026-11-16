extern int DAT_010729c8;
struct ValueRow {
    float __thiscall FUN_00a011b0(unsigned int key, unsigned int mode);
    void __thiscall FUN_00a012d0(unsigned int key, float value);
    void __thiscall FUN_00715c60(unsigned int key, unsigned int value);
    void __thiscall FUN_00a01350(unsigned int key, unsigned int value, unsigned int mode);
};
struct EntryList {
    int __thiscall FUN_00559450();
    ValueRow** __thiscall FUN_0057cbe0(int* iterator);
    void __thiscall FUN_004ed8c0(ValueRow** item);
};
struct FUN_00767ef0_shell {
    ValueRow* __thiscall FUN_00a1ddb0(void* owner, int* descriptor, unsigned int mode);
    void __thiscall FUN_00767ef0(unsigned int count, const unsigned int* values);
};
void __thiscall FUN_00767ef0_shell::FUN_00767ef0(unsigned int count, const unsigned int* values)
{
    ValueRow* item;
    {
        int iterator = ((EntryList*)((char*)this + 0x168))->FUN_00559450();
        while (iterator != 0) {
            item = *(((EntryList*)((char*)this + 0x168))->FUN_0057cbe0(&iterator));
            item->FUN_00a012d0(0xfac, item->FUN_00a011b0(0xfac, 1) + float(count));
        }
    }
    for (unsigned int index = 0; index < count; ++index) {
        item = FUN_00a1ddb0(*(void**)((char*)this + 0x118), &DAT_010729c8, 0);
        item->FUN_00715c60(0xfac, count - index - 1);
        item->FUN_00a01350(0xfc4, values[index], 1);
        ((EntryList*)((char*)this + 0x168))->FUN_004ed8c0(&item);
    }
}
