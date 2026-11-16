extern "C" void* __cdecl FUN_00aa13e0(unsigned int);
extern int DAT_0102016c;
extern int DAT_0102009c;
extern int DAT_010c9634;
extern int DAT_01268154;
extern int DAT_01268118;
extern int DAT_012685b8;

struct PhysicsElement {
    void* vtable;
    unsigned int referenceCount;
    unsigned int flags;
    unsigned int payload;

    void __thiscall FUN_00c87c30();

    static void* __cdecl operator new(unsigned int size) {
        return FUN_00aa13e0(size);
    }
    static void __cdecl operator delete(void*);

    PhysicsElement() {
        FUN_00c87c30();
        vtable = &DAT_0102016c;
        payload = 0;
        ++DAT_01268154;
        vtable = &DAT_0102009c;
        ++DAT_01268118;
        vtable = &DAT_010c9634;
        ++DAT_012685b8;
    }
};

PhysicsElement* __cdecl FUN_00cc33a0() {
    return new PhysicsElement();
}