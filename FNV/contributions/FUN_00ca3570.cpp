#include "h_74712c1d3c73.h"

struct FUN_00a5d3d0_class {
    void __thiscall FUN_00a5d3d0();
};

struct FUN_00ca3570_class : FUN_00a5d3d0_class {
    void* m_vtbl;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    void* unk14;
    void* unk18;
    void* unk1c;
    void* unk20;
    void* unk24;

    void __thiscall FUN_00ca3570();
};

extern "C" char DAT_010c740c[];
extern MemoryManager _g_memoryManager;

void __thiscall FUN_00ca3570_class::FUN_00ca3570()
{
    m_vtbl = DAT_010c740c;

    if (unk14)
        _g_memoryManager.Deallocate(unk14);

    if (unk18)
        _g_memoryManager.Deallocate(unk18);

    if (unk24)
        _g_memoryManager.Deallocate(unk24);

    if (unk20)
        _g_memoryManager.Deallocate(unk20);

    FUN_00a5d3d0_class::FUN_00a5d3d0();
}