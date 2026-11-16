struct DtorOwner00685e80 {
    void FUN_00a81bd0();
};
typedef void (__thiscall DtorOwner00685e80::*DtorMemberPointer)();
extern void __stdcall FUN_0065ee50_Helper(void* object, unsigned int size, int count, DtorMemberPointer destructor);
void __cdecl operator delete(void* p);
struct FUN_00685e80_Class {
    void* FUN_00685e80(unsigned int flags);
};
void* FUN_00685e80_Class::FUN_00685e80(unsigned int flags) {
    if (flags & 2) {
        FUN_0065ee50_Helper(this, 0x2c, *(int*)((char*)this - 4), &DtorOwner00685e80::FUN_00a81bd0);
        if (flags & 1)
            operator delete((char*)this - 4);
        return (char*)this - 4;
    }
    ((DtorOwner00685e80*)this)->FUN_00a81bd0();
    if (flags & 1)
        operator delete(this);
    return this;
}
