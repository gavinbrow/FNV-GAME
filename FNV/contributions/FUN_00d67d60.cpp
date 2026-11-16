struct Heap { virtual void* unused(); virtual void* Allocate(unsigned int); };
struct Global { int unk00; int unk04; int unk08; int unk0c; Heap* heap10; };
extern void* FUN_00c85750();
struct hkpToiCountViewer {
    void* vtable;
    unsigned short size;
    unsigned short unk06;
    hkpToiCountViewer* __thiscall FUN_00d67ce0(unsigned int);
};
void* __cdecl FUN_00d67d60(unsigned int arg) {
    Global* global = (Global*)FUN_00c85750();
    hkpToiCountViewer* object = (hkpToiCountViewer*)global->heap10->Allocate(0x40);
    object->size = 0x40;
    object = object->FUN_00d67ce0(arg);
    if (object) return (char*)object + 8;
    return 0;
}
