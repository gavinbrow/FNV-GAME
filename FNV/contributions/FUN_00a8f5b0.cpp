
extern void* __cdecl FUN_00aa13e0(unsigned int);
extern "C" void __fastcall FUN_00a5c200(void*);
extern int DAT_0109f68c;
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
extern "C" __declspec(dllimport) long __stdcall InterlockedIncrement(volatile long*);

struct NiPropertyMem;
struct NiPropertyVTable {
    void* reserved;
    void (__thiscall *dispose)(NiPropertyMem*);
};
struct NiPropertyMem {
    void* vtable;
    volatile long refs;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    unsigned short flags;

    __forceinline void DecRefCount() {
        if (InterlockedDecrement(&refs) == 0) {
            static_cast<NiPropertyVTable*>(vtable)->dispose(this);
        }
    }
    __forceinline void IncRefCount() {
        InterlockedIncrement(&refs);
    }
};
struct NiPointerProperty {
    NiPropertyMem* pointer;
    __forceinline void operator=(NiPropertyMem* fresh) {
        if (pointer != fresh) {
            if (pointer) pointer->DecRefCount();
            pointer = fresh;
            if (pointer) pointer->IncRefCount();
        }
    }
};
struct GlobalObjectO2_00a7b610 {
    int unk00;
    int unk04;
    NiPointerProperty cullingProperty;
};

void __cdecl FUN_00a8f5b0()
{
    NiPropertyMem* allocated = static_cast<NiPropertyMem*>(FUN_00aa13e0(sizeof(NiPropertyMem)));
    NiPropertyMem* fresh;
    if (allocated) {
        FUN_00a5c200(allocated);
        allocated->flags &= 0xfffe;
        allocated->vtable = &DAT_0109f68c;
        fresh = allocated;
    } else {
        fresh = 0;
    }
    g_011f5d20.cullingProperty = fresh;
}
