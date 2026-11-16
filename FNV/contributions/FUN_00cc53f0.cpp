
extern void* __cdecl FUN_00aa13e0(unsigned int);
extern "C" void __cdecl FUN_00c876f0();
extern "C" void __cdecl FUN_00c87700();
extern int DAT_0108febc;
extern int DAT_010c9a14;
extern int DAT_01268188;
extern int DAT_012685e8;
extern __declspec(thread) int hkThreadAllocationFlag;

struct HavokRuntimeObject {
    void* vtable;
    int refCount;
    int heapFlags;
    int extra;
    void __thiscall FUN_00c87c30();
    static void* __cdecl operator new(unsigned int size) { return FUN_00aa13e0(size); }
    HavokRuntimeObject() {
        FUN_00c87c30();
        vtable = &DAT_0108febc;
        extra = 0;
        ++DAT_01268188;
        vtable = &DAT_010c9a14;
        ++DAT_012685e8;
    }
};
struct HavokThreadScope {
    int oldValue;
    HavokThreadScope() {
        oldValue = hkThreadAllocationFlag;
        hkThreadAllocationFlag = 16;
    }
    ~HavokThreadScope() {
        FUN_00c87700();
        hkThreadAllocationFlag = oldValue;
    }
};
struct HavokAllocator {
    void* __thiscall FUN_00c89730(HavokRuntimeObject*, int);
    HavokRuntimeObject* __thiscall FUN_00cc53f0(int argument);
};
HavokRuntimeObject* __thiscall HavokAllocator::FUN_00cc53f0(int argument) {
    HavokThreadScope scope;
    FUN_00c876f0();
    HavokRuntimeObject* obj = new HavokRuntimeObject;
    FUN_00c89730(obj, argument);
    return obj;
}
