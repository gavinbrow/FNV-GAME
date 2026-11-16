
extern __declspec(thread) int g_memoryContext;
void __cdecl FUN_00c876f0();
void __cdecl FUN_00c87700();
void* __cdecl FUN_00aa13e0(unsigned int size);
struct AutoMemContext {
    int oldContext;
    AutoMemContext() {
        oldContext = g_memoryContext;
        g_memoryContext = 16;
    }
    ~AutoMemContext() {
        g_memoryContext = oldContext;
    }
};
struct FUN_00cbc550_class {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
    static void* __cdecl operator new(unsigned int size) {
        return FUN_00aa13e0(size);
    }
    FUN_00cbc550_class();
};
struct FUN_00cbca20_class {
    void __thiscall FUN_00c86800(FUN_00cbc550_class* obj, int flags);
    FUN_00cbc550_class* __thiscall FUN_00cbca20(int flags);
};
FUN_00cbc550_class* __thiscall FUN_00cbca20_class::FUN_00cbca20(int flags) {
    AutoMemContext context;
    FUN_00c876f0();
    FUN_00cbc550_class* result = new FUN_00cbc550_class();
    FUN_00c86800(result, flags);
    FUN_00c87700();
    return result;
}
