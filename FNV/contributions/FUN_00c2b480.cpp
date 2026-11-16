struct NiMemObject { static void* __cdecl operator new(unsigned int); };
struct CloneShell;
struct FUN_00c32d80 {
    virtual void base0();
    FUN_00c32d80();
    void FUN_00c32de0(CloneShell*, void*);
};
struct CloneShell : FUN_00c32d80 { virtual ~CloneShell() throw(); };
inline void* __cdecl operator new(unsigned int, void* memory) { return memory; }
struct C_00c2b480 : FUN_00c32d80 { CloneShell* FUN_00c2b480(void* volatile argument); };
CloneShell* C_00c2b480::FUN_00c2b480(void* volatile argument)
{
    CloneShell* clone = (CloneShell*)NiMemObject::operator new(0x40);
    if (clone) {
        new ((void*)clone) CloneShell;
        FUN_00c32de0(clone, argument);
    } else {
        void* processCopy = argument;
        clone = 0;
        FUN_00c32de0(clone, processCopy);
    }
    return clone;
}
