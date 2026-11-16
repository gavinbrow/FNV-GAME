// Candidate: FUN_00e8f7c0 — release/destructor-like routine for a render-object class.
// Stores the class vtable, calls two module-level helpers, and optionally
// unregisters the object from the global registry object at DAT_011f6238.

extern unsigned char DAT_010f02b0[];

struct FUN_00aa4060_Class {
    void __thiscall FUN_00aa4060(void* object);
};

extern FUN_00aa4060_Class DAT_011f6238;

void __cdecl FUN_00b601a0();
void __cdecl FUN_00aa10f0(void* data);

struct FUN_00e8f7c0_Class {
    void* m_vptr;
    char m_pad[4];
    void* m_data;

    void* FUN_00e8f7c0(unsigned char deleting);
};

void* FUN_00e8f7c0_Class::FUN_00e8f7c0(unsigned char deleting)
{
    m_vptr = (void*)&DAT_010f02b0;
    FUN_00b601a0();
    FUN_00aa10f0(m_data);
    if (deleting & 1) {
        DAT_011f6238.FUN_00aa4060(this);
    }
    return this;
}
