struct HandlerOperations {
    ListNodeHelper* FUN_00460140();
    unsigned char FUN_004516b0();
    TESObjectCELL* FUN_00461330(void* initializer, int x, int y, TESWorldSpace* space);
};
struct WorldOperations { TESObjectCELL* FUN_005875a0(int x, int y); };
extern "C" void __cdecl FUN_005b5e40(const void*, int, int);
extern char UNK_010187a0;
extern char UNK_01011584;
TESObjectCELL* FUN_00461c20_Holder::FUN_00461c20(int x, int y, TESWorldSpace* world, bool createMissing)
{
    if (!world) {
        world = (TESWorldSpace*)*(((HandlerOperations*)this)->FUN_00460140()->FUN_006815c0());
        if (!world) return 0;
    }
    if (x > 32767 || y > 32767 || x < -32768 || y < -32768) {
        FUN_005b5e40(&UNK_010187a0, -32768, 32767);
        return 0;
    }
    TESObjectCELL* cell = ((WorldOperations*)world)->FUN_005875a0(x, y);
    if (cell) return cell;
    if (!((HandlerOperations*)this)->FUN_004516b0() && createMissing)
        return ((HandlerOperations*)this)->FUN_00461330(&UNK_01011584, x, y, world);
    else
        return 0;
}