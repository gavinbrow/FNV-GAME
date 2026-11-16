
extern __declspec(thread) unsigned int memoryCategory;
extern int DAT_01030bf4, DAT_010c44e4, DAT_010c485c;
extern int DAT_012680f8, DAT_012686d0, DAT_012681a0;
void __cdecl FUN_00c876f0();
void __cdecl FUN_00c87700();
void* __cdecl FUN_00aa13e0(unsigned int size);
struct NewShape {
    int* vtable;
    int field04, field08, field0c, field10;
    static void* operator new(unsigned int size) { return FUN_00aa13e0(size); }
    void __thiscall FUN_00c87c30();
    NewShape() {
        FUN_00c87c30();
        vtable = &DAT_01030bf4;
        field0c = 0;
        field10 = 0;
        ++DAT_012680f8;
        vtable = &DAT_010c44e4;
        ++DAT_012686d0;
        vtable = &DAT_010c485c;
        ++DAT_012681a0;
    }
};
struct MemoryCategoryScope {
    unsigned int previous;
    MemoryCategoryScope() : previous(memoryCategory) { memoryCategory = 16; }
    ~MemoryCategoryScope() { memoryCategory = previous; }
};
struct FUN_00c8af10_holder {
    unsigned int* __thiscall FUN_00c8af10(unsigned int param);
};
unsigned int* __thiscall FUN_00c8af10_holder::FUN_00c8af10(unsigned int param) {
    MemoryCategoryScope scope;
    FUN_00c876f0();
    NewShape* result = new NewShape;
    typedef void (__thiscall *Dispatch)(FUN_00c8af10_holder*, NewShape*, unsigned int);
    void** vtable = *(void***)this;
    ((Dispatch)vtable[49])(this, result, param);
    FUN_00c87700();
    return (unsigned int*)result;
}