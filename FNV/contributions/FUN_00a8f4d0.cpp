extern int DAT_0109f584;
extern int DAT_0101dce4;
extern char* DAT_0109b220;
extern volatile long DAT_011f4400;
__declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
void __cdecl FUN_00aa1460(void*, unsigned int);

struct FUN_00a8f4d0_shell {
    int* volatile vtable;
    unsigned int instanceId;
    char* volatile text;
    FUN_00a8f4d0_shell* FUN_00a8f4d0(unsigned char flags);
};

FUN_00a8f4d0_shell* FUN_00a8f4d0_shell::FUN_00a8f4d0(unsigned char flags) {
    vtable = &DAT_0109f584;
    char* stringData = text;
    if (stringData != DAT_0109b220)
        InterlockedDecrement(reinterpret_cast<volatile long*>(stringData - 8));
    vtable = &DAT_0101dce4;
    InterlockedDecrement(&DAT_011f4400);
    if (flags & 1)
        FUN_00aa1460(this, 20);
    return this;
}