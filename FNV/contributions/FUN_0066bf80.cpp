struct FUN_0066bf80_vftable {
    void* slot000;
    void* slot004;
    void* slot008;
    void* slot00C;
    void* slot010;
    void* slot014;
    void* slot018;
    void* slot01C;
    void* slot020;
    void* slot024;
    void* slot028;
    void* slot02C;
    void* slot030;
    void* slot034;
    void* slot038;
    void* slot03C;
    void* slot040;
    void* slot044;
    void* slot048;
    void* slot04C;
    void* slot050;
    void* slot054;
    void* slot058;
    void* slot05C;
    void* slot060;
    void* slot064;
    void* slot068;
    void* slot06C;
    void* slot070;
    void* slot074;
    void* slot078;
    void* slot07C;
    void* slot080;
    void* slot084;
    void* slot088;
    void* slot08C;
    void* slot090;
    void* slot094;
    void* slot098;
    void* slot09C;
    void* slot0A0;
    void* slot0A4;
    void* slot0A8;
    void* slot0AC;
    void* slot0B0;
    void* slot0B4;
    void* slot0B8;
    void* slot0BC;
    void* slot0C0;
    void* slot0C4;
    void* slot0C8;
    void* slot0CC;
    void* slot0D0;
    void* slot0D4;
    void* slot0D8;
    void* slot0DC;
    void* slot0E0;
    void* slot0E4;
    void* slot0E8;
    void* slot0EC;
    void* slot0F0;
    void* slot0F4;
    void* slot0F8;
    void* slot0FC;
    void* slot100;
    void* slot104;
    void* slot108;
    void* slot10C;
    void* slot110;
    void* slot114;
    void* slot118;
    void* slot11C;
    void* slot120;
    void* slot124;
    void* slot128;
    void* slot12C;
    void* slot130;
    void* slot134;
    void* slot138;
    void* slot13C;
    void* slot140;
    void (__thiscall *process)(void*, float);
};
struct FUN_0066bf80_owner {
    FUN_0066bf80_vftable* vtable;
    void __thiscall FUN_0066bf80(struct FUN_0066bf80_data*, unsigned int);
};
struct FUN_0066bf80_data { float time; };
struct NiCamera;
extern double gModifierZero;
struct FUN_00a5dd70_shell { void __thiscall FUN_00a5dd70(FUN_0066bf80_data&, unsigned int); };
extern "C" unsigned int __cdecl FUN_00552380();
extern bool __cdecl FUN_004b5fc0(NiAVObject*, NiCamera*);
enum MEM_CONTEXT { MEM_CONTEXT_SCENE = 0x1e };
struct AutoMemContext {
    AutoMemContext(MEM_CONTEXT, bool, const char*, int);
    ~AutoMemContext();
    int state;
};
void FUN_0066bf80_owner::FUN_0066bf80(FUN_0066bf80_data* data, unsigned int flags) {
    AutoMemContext context(MEM_CONTEXT_SCENE, true, "D:\\_Fallout3\\Platforms\\Common\\Code\\Fallout Shared\\SpeedTree\\BSTreeNode.cpp", 0x20d);
    if (!FUN_0054ee20())
        return;
    if (data->time > gModifierZero) {
        if (!FUN_004b5fc0((NiAVObject*)this, (NiCamera*)FUN_00552380()))
            return;
    }
    vtable->process(this, data->time);
    ((FUN_00a5dd70_shell*)this)->FUN_00a5dd70(*data, flags);
}



