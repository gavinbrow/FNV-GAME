extern char DAT_01096694;
void* __cdecl FUN_00aa13e0(unsigned int size) throw();

struct FUN_00a2f8c0 {
    void* vtable;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
    unsigned int unk30;
    FUN_00a2f8c0() throw();
};

struct TreadInterpolator : FUN_00a2f8c0 {
    unsigned int unk34;
    unsigned short unk38;
    unsigned short unk3a;
    unsigned int unk3c;
    unsigned short unk40;
    unsigned short unk42;

    static void* operator new(unsigned int size) throw() { return FUN_00aa13e0(size); }
    TreadInterpolator() throw() {
        vtable = &DAT_01096694;
        unk34 = 0;
        unk38 = 0;
        unk40 = 0;
        unk3c = 0;
    }
};

struct TreadController {
    TreadInterpolator* __thiscall FUN_00a35a10(unsigned int index);
    void __thiscall FUN_00a2f8a0(TreadInterpolator* interp, unsigned int index);
};

TreadInterpolator* TreadController::FUN_00a35a10(unsigned int index)
{
    TreadInterpolator* interp = new TreadInterpolator;
    FUN_00a2f8a0(interp, index);
    return interp;
}