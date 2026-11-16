// @fnv 0x00fde350
struct Obj {
    int pad[24];
    int count;
    void __thiscall FUN_00e7ecd0();
    void Release() { --count; if (count == 0) FUN_00e7ecd0(); }
};
extern Obj* DAT_0126f730;
void FUN_00fde350()
{
    if (DAT_0126f730) DAT_0126f730->Release();
}
