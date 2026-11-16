void __cdecl __debugbreak();
struct MessageBuffer { char* begin; char* end; unsigned int capacity; };
struct FUN_00cb1600_class { void FUN_00cb1600(char* storage, unsigned int size); };
struct FUN_00cc01c0_class {
    FUN_00cc01c0_class* FUN_00cc01c0(const char* text);
    FUN_00cc01c0_class* FUN_00cc0120(const void* value);
    FUN_00cc01c0_class* FUN_00cc0280(int value);
};
struct FUN_00cc00e0_class { void FUN_00cc00e0(); };
struct ErrorReporter {
    virtual void vfn_00();
    virtual void vfn_04();
    virtual void vfn_08();
    virtual int Report(int severity, unsigned int category, const char* text, const char* file, int line);
};
extern ErrorReporter* DAT_01268360;
void __cdecl FUN_00cb1660(const void* object, const char* context)
{
    MessageBuffer message;
    unsigned int storage[128];
    ((FUN_00cb1600_class*)&message)->FUN_00cb1600((char*)storage, 0x200);
    int referenceCount = *(const short*)((const char*)object + 6);
    ((FUN_00cc01c0_class*)&message)->FUN_00cc01c0("Reference count error on object ")
        ->FUN_00cc0120(object)
        ->FUN_00cc01c0(" with ref count of ")
        ->FUN_00cc0280(referenceCount)
        ->FUN_00cc01c0(" in ")
        ->FUN_00cc01c0(context)
        ->FUN_00cc01c0(".\n")
        ->FUN_00cc01c0(" * Are you calling delete instead of removeReference?\n")
        ->FUN_00cc01c0(" * Have you called removeReference too many times?\n")
        ->FUN_00cc01c0(" * In a multithreaded environment, what is the hkReferencedObject lock mode you use (see setLockMode())?\n")
        ->FUN_00cc01c0(" * Is this a valid object?\n")
        ->FUN_00cc01c0(" * Do you have more than 32768 references? (unlikely)\n");
    if (DAT_01268360->Report(3, 0x2c66f2d8, (char*)storage, ".\\System\\Error\\hkError.cpp", 0x21))
        __debugbreak();
    ((FUN_00cc00e0_class*)&message)->FUN_00cc00e0();
}



